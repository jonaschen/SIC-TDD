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
        start_pc = 0x2000
        store_address = 0x2080
        value_to_store = 0xCCBBFF

        self.registers.A = value_to_store
        self.registers.PC = start_pc
        self.memory.write_word(start_pc, 0x0C2080) # STA 0x2080

        # --- Execution ---
        self.cpu.step()

        # --- Verification ---
        self.assertEqual(self.memory.read_word(store_address), value_to_store, "Memory should contain the value from register A.")
        self.assertEqual(self.registers.PC, start_pc + 3, "PC should be incremented by 3.")

    def test_step_executes_add_instruction(self):
        """
        Tests the full fetch-decode-execute cycle for a single ADD instruction.
        """
        # --- Setup ---
        # Program: ADD 0x3050
        start_pc = 0x3000
        data_address = 0x3050
        
        initial_a_value = 0x000010
        value_to_add = 0x000025
        expected_result = 0x000035

        self.registers.A = initial_a_value
        self.registers.PC = start_pc
        self.memory.write_word(data_address, value_to_add)
        self.memory.write_word(start_pc, 0x183050) # ADD 0x3050

        # --- Execution ---
        self.cpu.step()

        # --- Verification ---
        self.assertEqual(self.registers.A, expected_result, "Register A should hold the sum.")
        self.assertEqual(self.registers.PC, start_pc + 3, "PC should be incremented by 3.")

    def test_step_executes_sub_instruction(self):
        """
        Tests the full fetch-decode-execute cycle for a single SUB instruction.
        """
        # --- Setup ---
        # Program: SUB 0x4050
        start_pc = 0x4000
        data_address = 0x4050
        
        initial_a_value = 0x000035
        value_to_sub = 0x000010
        expected_result = 0x000025

        self.registers.A = initial_a_value
        self.registers.PC = start_pc
        self.memory.write_word(data_address, value_to_sub)
        self.memory.write_word(start_pc, 0x1C4050) # SUB 0x4050

        # --- Execution ---
        self.cpu.step()

        # --- Verification ---
        self.assertEqual(self.registers.A, expected_result, "Register A should hold the difference.")
        self.assertEqual(self.registers.PC, start_pc + 3, "PC should be incremented by 3.")

    def test_step_executes_comp_instruction(self):
        """
        Tests the COMP instruction for all three conditions (<, =, >).
        Opcode for COMP is 0x28.
        """
        start_pc = 0x5000
        data_address = 0x5050
        
        # --- Test Case 1: A < memory ---
        self.registers.A = 10
        self.memory.write_word(data_address, 20)
        self.registers.PC = start_pc
        self.memory.write_word(start_pc, 0x285050) # COMP 0x5050
        self.cpu.step()
        self.assertEqual(self.registers.SW, ord('<'), "SW should be '<' for A < memory.")
        self.assertEqual(self.registers.PC, start_pc + 3)

        # --- Test Case 2: A == memory ---
        self.registers.A = 20
        self.memory.write_word(data_address, 20)
        self.registers.PC = start_pc
        self.memory.write_word(start_pc, 0x285050) # COMP 0x5050
        self.cpu.step()
        self.assertEqual(self.registers.SW, ord('='), "SW should be '=' for A == memory.")
        self.assertEqual(self.registers.PC, start_pc + 3)

        # --- Test Case 3: A > memory ---
        self.registers.A = 30
        self.memory.write_word(data_address, 20)
        self.registers.PC = start_pc
        self.memory.write_word(start_pc, 0x285050) # COMP 0x5050
        self.cpu.step()
        self.assertEqual(self.registers.SW, ord('>'), "SW should be '>' for A > memory.")
        self.assertEqual(self.registers.PC, start_pc + 3)

    def test_step_executes_j_instruction(self):
        """
        Tests the J (unconditional jump) instruction.
        Opcode for J is 0x3C.
        """
        # --- Setup ---
        # Program: J 0x6050
        start_pc = 0x6000
        target_address = 0x6050

        self.registers.PC = start_pc
        self.memory.write_word(start_pc, 0x3C6050) # J 0x6050

        # --- Execution ---
        self.cpu.step()

        # --- Verification ---
        # The PC should be set to the target address, not start_pc + 3.
        self.assertEqual(self.registers.PC, target_address, "PC should be updated to the jump target address.")

    def test_step_executes_jeq_instruction(self):
        """
        Tests the JEQ (Jump if Equal) instruction.
        Opcode for JEQ is 0x30.
        """
        start_pc = 0x7000
        target_address = 0x7050
        
        # --- Test Case 1: Jump is taken (SW == '=') ---
        self.registers.SW = ord('=')
        self.registers.PC = start_pc
        self.memory.write_word(start_pc, 0x307050) # JEQ 0x7050
        self.cpu.step()
        self.assertEqual(self.registers.PC, target_address, "JEQ should jump when SW is '='.")

        # --- Test Case 2: Jump is NOT taken (SW != '=') ---
        self.registers.SW = ord('<') # Condition is not met
        self.registers.PC = start_pc
        self.memory.write_word(start_pc, 0x307050) # JEQ 0x7050
        self.cpu.step()
        self.assertEqual(self.registers.PC, start_pc + 3, "JEQ should not jump when SW is not '='.")


if __name__ == '__main__':
    unittest.main()
