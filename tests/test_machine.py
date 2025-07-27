import unittest
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.machine import SICMachine

class TestMachine(unittest.TestCase):
    """
    Test suite for the integrated SIC Machine.
    """

    def setUp(self):
        """
        Set up a new Machine instance for each test.
        """
        self.machine = SICMachine()

    def test_machine_initialization(self):
        """
        Tests that the machine initializes its components correctly.
        """
        self.assertIsNotNone(self.machine.memory)
        self.assertIsNotNone(self.machine.registers)
        self.assertIsNotNone(self.machine.cpu)

    def test_load_program(self):
        """
        Tests that a program can be loaded into the machine's memory.
        """
        program = [
            0x00100C, # LDA FIVE
            0x18100F, # ADD THREE
            0x0C1012, # STA RESULT
        ]
        start_address = 0x1000
        
        self.machine.load_program(program, start_address)

        # Verify that the instructions are in memory
        self.assertEqual(self.machine.memory.read_word(0x1000), 0x00100C)
        self.assertEqual(self.machine.memory.read_word(0x1003), 0x18100F)
        self.assertEqual(self.machine.memory.read_word(0x1006), 0x0C1012)

    def test_run_simple_program(self):
        """
        An integration test to run a simple program and verify the result.
        The program adds 5 + 3 and stores the result.
        """
        # --- Program and Data ---
        program_start = 0x1000
        data_start = 0x100C

        # Instructions
        program = [
            0x00100C, # 1000: LDA FIVE
            0x18100F, # 1003: ADD THREE
            0x0C1012, # 1006: STA RESULT
        ]
        
        # Data
        five = 5
        three = 3
        
        # --- Loading ---
        self.machine.load_program(program, program_start)
        self.machine.memory.write_word(data_start, five)     # 100C: FIVE
        self.machine.memory.write_word(data_start + 3, three) # 100F: THREE
        self.machine.registers.PC = program_start

        # --- Execution ---
        # Run for 3 steps, one for each instruction
        self.machine.run(steps=3)

        # --- Verification ---
        # The final result (8) should be stored at address 0x1012
        result_address = 0x1012
        self.assertEqual(self.machine.memory.read_word(result_address), 8)
        # PC should be at the end of the program
        self.assertEqual(self.machine.registers.PC, program_start + 9)

    def test_step_method(self):
        """Tests that the step method executes a single instruction."""
        program_start = 0x1000
        data_address = 0x100C
        five = 5

        # LDA FIVE
        self.machine.memory.write_word(program_start, 0x00100C)
        self.machine.memory.write_word(data_address, five)
        self.machine.registers.PC = program_start

        self.machine.step() # Use the new step method

        self.assertEqual(self.machine.registers.A, five)
        self.assertEqual(self.machine.registers.PC, program_start + 3)

    def test_reset_machine(self):
        """Tests that the reset method clears the machine state."""
        # Modify the state
        self.machine.registers.A = 123
        self.machine.memory.write_byte(100, 45)

        # Reset the machine
        self.machine.reset()

        # Verify state is cleared
        self.assertEqual(self.machine.registers.A, 0)
        self.assertEqual(self.machine.memory.read_byte(100), 0)
        self.assertIsNot(self.machine.registers.A, 123, "Register should be reset.")


if __name__ == '__main__':
    unittest.main()
