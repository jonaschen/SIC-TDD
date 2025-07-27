from .memory import Memory
from .registers import Registers
from .cpu import CPU

class SICMachine:
    """
    Integrates all components of the SIC emulator into a working virtual machine.
    This class orchestrates the overall operation.
    """

    def __init__(self):
        """
        Initializes the entire SIC machine, creating instances of
        Memory, Registers, and CPU.
        """
        self.memory = Memory()
        self.registers = Registers()
        self.cpu = CPU(self.registers, self.memory)

    def reset(self):
        """
        Resets the machine to its initial state by re-initializing all components.
        """
        self.__init__()

    def step(self):
        """
        Executes a single instruction cycle by calling the CPU's step method.
        """
        self.cpu.step()

    def load_program(self, program: list[int], start_address: int):
        """
        Loads a list of instruction words into memory.
        
        Args:
            program: A list of 24-bit integers representing the program.
            start_address: The memory address where loading should begin.
        """
        current_address = start_address
        for word in program:
            self.memory.write_word(current_address, word)
            current_address += 3

    def run(self, steps: int = 100):
        """
        Runs the CPU's fetch-decode-execute cycle for a given number of steps.
        
        Args:
            steps: The maximum number of instructions to execute.
        """
        for _ in range(steps):
            self.step()

