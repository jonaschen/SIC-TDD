from .registers import Registers
from .memory import Memory
from .instruction import Instruction
from .devices import DeviceManager

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
        } 

    def fetch(self) -> Instruction:
        """
        Fetches a 3-byte instruction from memory at the address
        specified by the Program Counter (PC).
        """
        instruction_address = self.registers.PC
        instruction_word = self.memory.read_word(instruction_address)
        return Instruction(instruction_word)

    def step(self):
        """
        Executes a single fetch-decode-execute cycle.
        """
        # 1. Fetch
        instr = self.fetch()

        # 2. Increment Program Counter
        # The PC is normally incremented after fetching.
        # For successful jump instructions, this value will be overwritten.
        self.registers.PC += 3

        # 3. Decode and Execute
        handler = self.opcodes.get(instr.opcode)
        if handler:
            handler(instr)
        else:
            raise NotImplementedError(f"Opcode {instr.opcode:02X} is not implemented.")

    # --- Instruction Handlers ---

    def _get_effective_address(self, instr: Instruction) -> int:
        """
        Calculates the effective address for an instruction,
        handling indexed addressing mode.
        """
        address = instr.address
        if instr.x == 1:
            address += self.registers.X
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
