from .registers import Registers
from .memory import Memory
from .instruction import Instruction
from .devices import DeviceManager

class ProtectionError(Exception):
    """Exception raised for memory protection or privileged instruction violations."""
    def __init__(self, interrupt_code):
        self.interrupt_code = interrupt_code

class CPU:
    """
    Represents the Central Processing Unit of the SIC machine.
    It orchestrates the fetch-decode-execute cycle.
    """

    def __init__(self, registers: Registers, memory: Memory, device_manager: DeviceManager = None):
        """
        Initializes the CPU with references to the registers, memory, and device manager.
        
        Args:
            registers: The machine's register file.
            memory: The machine's main memory.
            device_manager: The machine's IO device manager.
        """
        self.registers = registers
        self.memory = memory
        self.device_manager = device_manager
        # Map opcodes to their handler methods.
        self.opcodes = {
            0x00: self._lda,
            0x0C: self._sta,
            0x18: self._add,
            0x1C: self._sub,
            0x28: self._comp,
            0x3C: self._j,
            0x30: self._jeq,
            0xD8: self._rd,
            0xDC: self._wd,
            0xE0: self._td,
            0xB0: self._svc,
            0xD0: self._lps,
        } 

    # Mapping of opcodes to their instruction formats (length in bytes)
    FORMAT_MAP = {
        0xB0: 2,  # SVC
    }

    # Privileged opcodes
    PRIVILEGED_OPCODES = {0xD8, 0xDC, 0xE0, 0xD0} # RD, WD, TD, LPS

    def _check_memory_protection(self, address: int):
        """
        Checks if the address is protected and if the current mode allows access.
        Raises an interrupt if protection is violated.
        """
        if self.registers.mode == Registers.USER and address < 0x1000:
            raise ProtectionError(2) # Code 2: Memory Protection Violation

    def fetch(self) -> Instruction:
        """
        Fetches an instruction from memory at the address
        specified by the Program Counter (PC).
        """
        instruction_address = self.registers.PC
        # Read the first byte to determine the opcode and format
        first_byte = self.memory.read_byte(instruction_address)

        format = self.FORMAT_MAP.get(first_byte, 3)

        if format == 2:
            second_byte = self.memory.read_byte(instruction_address + 1)
            word = (first_byte << 8) | second_byte
            return Instruction(word, format=2)
        else:
            # Assume Format 3 for everything else (standard SIC)
            word = self.memory.read_word(instruction_address)
            return Instruction(word, format=3)

    def step(self):
        """
        Executes a single fetch-decode-execute cycle.
        """
        try:
            # 1. Memory Protection Check for PC
            self._check_memory_protection(self.registers.PC)

            # 2. Fetch
            instr = self.fetch()

            # 3. Increment Program Counter
            # The PC is normally incremented by the instruction length.
            # For successful jump instructions, this value will be overwritten.
            self.registers.PC += instr.format

            # 4. Privileged Instruction Check
            if self.registers.mode == Registers.USER and instr.opcode in self.PRIVILEGED_OPCODES:
                raise ProtectionError(1) # Code 1: Privileged Instruction Exception

            # 5. Decode and Execute
            handler = self.opcodes.get(instr.opcode)
            if handler:
                handler(instr)
            else:
                raise NotImplementedError(f"Opcode {instr.opcode:02X} is not implemented.")
        except ProtectionError as e:
            self._handle_interrupt(e.interrupt_code)

    # --- Instruction Handlers ---

    def _get_effective_address(self, instr: Instruction) -> int:
        """
        Calculates the effective address for an instruction,
        handling indexed addressing mode.
        """
        address = instr.address
        if instr.x == 1:
            address += self.registers.X

        self._check_memory_protection(address)
        return address

    def _lda(self, instr: Instruction):
        """
        Executes the LDA (Load Accumulator) instruction.
        Opcode: 0x00
        """
        effective_address = self._get_effective_address(instr)
        self.registers.A = self.memory.read_word(effective_address)

    def _sta(self, instr: Instruction):
        """
        Executes the STA (Store Accumulator) instruction.
        Opcode: 0x0C
        """
        effective_address = self._get_effective_address(instr)
        self.memory.write_word(effective_address, self.registers.A)

    def _add(self, instr: Instruction):
        """
        Executes the ADD (Add to Accumulator) instruction.
        Opcode: 0x18
        """
        effective_address = self._get_effective_address(instr)
        operand = self.memory.read_word(effective_address)
        self.registers.A += operand

    def _sub(self, instr: Instruction):
        """
        Executes the SUB (Subtract from Accumulator) instruction.
        Opcode: 0x1C
        """
        effective_address = self._get_effective_address(instr)
        operand = self.memory.read_word(effective_address)
        self.registers.A -= operand

    def _comp(self, instr: Instruction):
        """
        Executes the COMP (Compare) instruction.
        Opcode: 0x28
        Compares A with a word in memory and sets the SW register.
        """
        effective_address = self._get_effective_address(instr)
        operand = self.memory.read_word(effective_address)
        
        if self.registers.A < operand:
            self.registers.SW = ord('<')
        elif self.registers.A == operand:
            self.registers.SW = ord('=')
        else: # self.registers.A > operand
            self.registers.SW = ord('>')

    def _j(self, instr: Instruction):
        """
        Executes the J (Jump) instruction.
        Opcode: 0x3C
        """
        effective_address = self._get_effective_address(instr)
        self.registers.PC = effective_address

    def _jeq(self, instr: Instruction):
        """
        Executes the JEQ (Jump if Equal) instruction.
        Opcode: 0x30
        """
        if self.registers.SW == ord('='):
            effective_address = self._get_effective_address(instr)
            self.registers.PC = effective_address
        # If the condition is not met, the PC retains its incremented value from step().

    def _td(self, instr: Instruction):
        """
        Executes the TD (Test Device) instruction.
        Opcode: 0xE0
        Sets SW to '<' if ready, '=' if busy.
        """
        effective_address = self._get_effective_address(instr)
        device_id = effective_address & 0xFF
        device = self.device_manager.get_device(device_id) if self.device_manager else None

        if device and device.test():
            self.registers.SW = ord('<')
        else:
            self.registers.SW = ord('=')

    def _rd(self, instr: Instruction):
        """
        Executes the RD (Read Device) instruction.
        Opcode: 0xD8
        Reads a byte into the rightmost 8 bits of A.
        """
        effective_address = self._get_effective_address(instr)
        device_id = effective_address & 0xFF
        device = self.device_manager.get_device(device_id) if self.device_manager else None

        byte = device.read() if device else 0
        self.registers.A = (self.registers.A & 0xFFFF00) | (byte & 0xFF)

    def _wd(self, instr: Instruction):
        """
        Executes the WD (Write Device) instruction.
        Opcode: 0xDC
        Writes the rightmost 8 bits of A to the device.
        """
        effective_address = self._get_effective_address(instr)
        device_id = effective_address & 0xFF
        device = self.device_manager.get_device(device_id) if self.device_manager else None

        if device:
            device.write(self.registers.A & 0xFF)

    def _svc(self, instr: Instruction):
        """
        Executes the SVC (Supervisor Call) instruction.
        Opcode: 0xB0 (Format 2)
        Triggers a software interrupt with the code given by r1.
        """
        interrupt_code = instr.r1
        self._handle_interrupt(interrupt_code)

    def _lps(self, instr: Instruction):
        """
        Executes the LPS (Load Program Status) instruction.
        Opcode: 0xD0
        Loads SW and PC from memory.
        """
        effective_address = self._get_effective_address(instr)
        self.registers.SW = self.memory.read_word(effective_address)
        self.registers.PC = self.memory.read_word(effective_address + 3)

    def _handle_interrupt(self, interrupt_code: int):
        """
        Handles an interrupt or exception.
        Saves current SW and PC to memory (0x00 and 0x03).
        Loads new SW and PC from memory (0x06 and 0x09).
        The interrupt code is stored in the saved SW (bits 16-23).
        """
        # 1. Prepare saved SW with interrupt code
        saved_sw = self.registers.SW
        # Mask out any old interrupt code and set the new one
        saved_sw = (saved_sw & 0x00FFFF) | ((interrupt_code & 0xFF) << 16)

        # 2. Save current state
        self.memory.write_word(0x000000, saved_sw)
        self.memory.write_word(0x000003, self.registers.PC)

        # 3. Load new state from vectors
        self.registers.SW = self.memory.read_word(0x000006)
        self.registers.PC = self.memory.read_word(0x000009)

        # 4. Ensure we are in Supervisor mode (bit 6 of SW = 0)
        self.registers.mode = Registers.SUPERVISOR
