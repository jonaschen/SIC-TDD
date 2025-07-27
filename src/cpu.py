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
        # A mapping from opcode to execution method could be useful here.
        self.opcodes = {} 

    def fetch(self) -> Instruction:
        """
        Fetches a 3-byte instruction from memory at the address
        specified by the Program Counter (PC).
        """
        # To be implemented
        raise NotImplementedError("CPU fetch() method not implemented yet.")

    def step(self):
        """
        Executes a single fetch-decode-execute cycle.
        """
        # To be implemented
        raise NotImplementedError("CPU step() method not implemented yet.")

