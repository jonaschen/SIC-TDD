import unittest
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.cpu import CPU
from src.memory import Memory
from src.registers import Registers
from src.instruction import Instruction

class TestCPU(unittest.TestCase):
    """
    Test suite for the CPU component of the SIC computer.
    """

    def setUp(self):
        """
        Set up a new CPU, Memory, and Registers instance for each test.
        """
        self.memory = Memory()
        self.registers = Registers()
        self.cpu = CPU(self.registers, self.memory)

    def test_cpu_initialization(self):
        """
        Tests that the CPU is initialized correctly with memory and registers.
        """
        self.assertIsInstance(self.cpu, CPU)
        self.assertIs(self.cpu.memory, self.memory)
        self.assertIs(self.cpu.registers, self.registers)

    def test_fetch_instruction(self):
        """
        Tests the fetch part of the cycle.
        """
        # Arrange: Place an instruction word at address 0x2000
        self.memory.write_word(0x2000, 0x0C1234) # STA 0x1234
        self.registers.PC = 0x2000

        # Act: Fetch the instruction
        instr = self.cpu.fetch()

        # Assert: Check if the fetched instruction is correct
        self.assertIsInstance(instr, Instruction)
        self.assertEqual(instr.opcode, 0x0C)
        self.assertEqual(instr.address, 0x1234)

    def test_step_executes_lda_instruction(self):
        """
        Tests the full fetch-decode-execute cycle for a single LDA instruction.
        """
        # --- Setup ---
        # Program to execute: LDA 0x1050
        start_pc = 0x1000
        data_address = 0x1050
        data_value = 0xAA55FF

        self.registers.PC = start_pc
        self.memory.write_word(start_pc, 0x001050) # LDA 0x1050
        self.memory.write_word(data_address, data_value)

        # --- Execution ---
        self.cpu.step()

        # --- Verification ---
        self.assertEqual(self.registers.A, data_value, "Register A should be loaded with the value.")
        self.assertEqual(self.registers.PC, start_pc + 3, "PC should be incremented by 3.")

    def test_step_executes_sta_instruction(self):
        """
        Tests the full fetch-decode-execute cycle for a single STA instruction.
        """
        # --- Setup ---
        # Program to execute: STA 0x2080
        # Opcode for STA is 0x0C
        start_pc = 0x2000
        store_address = 0x2080
        value_to_store = 0xCCBBFF

        # Load a value into the A register
        self.registers.A = value_to_store
        self.registers.PC = start_pc

        # Place the instruction in memory: STA 0x2080 -> 0x0C2080
        self.memory.write_word(start_pc, 0x0C2080)

        # --- Execution ---
        self.cpu.step()

        # --- Verification ---
        # 1. The value from register A should be in memory at the target address.
        self.assertEqual(self.memory.read_word(store_address), value_to_store, "Memory should contain the value from register A.")

        # 2. The Program Counter should have advanced by 3.
        self.assertEqual(self.registers.PC, start_pc + 3, "PC should be incremented by 3.")


if __name__ == '__main__':
    unittest.main()
