from .memory import Memory
from .registers import Registers
from .cpu import CPU

class Machine:
    """
    Integrates all components of the SIC emulator into a working virtual machine.
    This class orchestrates the overall operation.
    """

    def __init__(self):
        """
        Initializes the entire SIC machine, creating instances of
        Memory, Registers, and CPU.
        """
        # To be implemented
        raise NotImplementedError

    def load_program(self, program: list[int], start_address: int):
        """
        Loads a list of instruction words into memory.
        
        Args:
            program: A list of 24-bit integers representing the program.
            start_address: The memory address where loading should begin.
        """
        # To be implemented
        raise NotImplementedError

    def run(self, steps: int = 100):
        """
        Runs the CPU's fetch-decode-execute cycle for a given number of steps.
        
        Args:
            steps: The maximum number of instructions to execute.
        """
        # To be implemented
        raise NotImplementedError
