import unittest
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.registers import Registers

class TestRegisters(unittest.TestCase):
    """
    Test suite for the Registers component of the SIC computer.
    """

    def setUp(self):
        """
        Create a new Registers instance before each test.
        """
        self.registers = Registers()

    def test_initial_register_values(self):
        """
        Test 1: Verifies that all SIC registers are initialized to 0.
        """
        self.assertEqual(self.registers.A, 0, "Register A should initialize to 0.")
        self.assertEqual(self.registers.X, 0, "Register X should initialize to 0.")
        self.assertEqual(self.registers.L, 0, "Register L should initialize to 0.")
        self.assertEqual(self.registers.PC, 0, "Register PC should initialize to 0.")
        self.assertEqual(self.registers.SW, 0, "Register SW should initialize to 0.")

    def test_set_and_get_registers(self):
        """
        Test 2: Verifies that values can be set and retrieved from registers.
        """
        self.registers.A = 0x123456
        self.registers.X = 0xABCDEF
        self.registers.PC = 0x4000

        self.assertEqual(self.registers.A, 0x123456)
        self.assertEqual(self.registers.X, 0xABCDEF)
        self.assertEqual(self.registers.PC, 0x4000)

    def test_register_value_truncation(self):
        """
        Test 3: Verifies that register values are automatically truncated to 24 bits.
        """
        self.registers.A = 0x99ABCDEF  # A 32-bit value
        expected_value = 0xABCDEF     # The lower 24 bits
        self.assertEqual(self.registers.A, expected_value, "Register A should be truncated to 24 bits.")

        self.registers.L = 0xFFFFFFFF
        self.assertEqual(self.registers.L, 0xFFFFFF, "Register L should be truncated to 24 bits.")

    def test_invalid_register_access(self):
        """
        Test 4: Verifies that accessing a non-existent register raises an AttributeError.
        """
        with self.assertRaises(AttributeError, msg="Accessing a non-existent register should raise an AttributeError."):
            _ = self.registers.Z

        with self.assertRaises(AttributeError, msg="Setting a non-existent register should raise an AttributeError."):
            self.registers.Z = 0


if __name__ == '__main__':
    unittest.main()
