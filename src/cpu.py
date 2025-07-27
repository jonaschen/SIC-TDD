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
        # The PC is incremented after fetching and before executing.
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

