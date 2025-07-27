from .registers import Registers
from .memory import Memory
from .instruction import Instruction

class CPU:
    """
    Represents the Central Processing Unit of the SIC machine.
    It orchestrates the fetch-decode-execute cycle.
    """

    def __init__(self, registers: Registers, memory: Memory):
        """
        Initializes the CPU with references to the registers and memory.
        
        Args:
            registers: The machine's register file.
            memory: The machine's main memory.
        """
        self.registers = registers
        self.memory = memory
        # Map opcodes to their handler methods.
        self.opcodes = {
            0x00: self._lda,
            0x0C: self._sta,
            0x18: self._add,
            0x1C: self._sub,
            0x28: self._comp,
            0x3C: self._j,
            0x30: self._jeq,
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

