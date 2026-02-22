import unittest
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.registers import Registers

class TestRegistersXE(unittest.TestCase):
    """
    Test suite for the additional registers (B, S, T, F) introduced in SIC/XE.
    """

    def setUp(self):
        """
        Create a new Registers instance before each test.
        """
        self.registers = Registers()

    def test_initial_values_xe(self):
        """
        Verifies that SIC/XE registers (B, S, T, F) are initialized to 0.
        """
        # Test B register (Base register)
        self.assertTrue(hasattr(self.registers, 'B'), "Register B should exist.")
        self.assertEqual(self.registers.B, 0, "Register B should initialize to 0.")

        # Test S register (General purpose)
        self.assertTrue(hasattr(self.registers, 'S'), "Register S should exist.")
        self.assertEqual(self.registers.S, 0, "Register S should initialize to 0.")

        # Test T register (General purpose)
        self.assertTrue(hasattr(self.registers, 'T'), "Register T should exist.")
        self.assertEqual(self.registers.T, 0, "Register T should initialize to 0.")

        # Test F register (Floating Point Accumulator)
        self.assertTrue(hasattr(self.registers, 'F'), "Register F should exist.")
        self.assertEqual(self.registers.F, 0, "Register F should initialize to 0.")

    def test_set_and_get_xe_registers(self):
        """
        Verifies that values can be set and retrieved from SIC/XE registers.
        """
        self.registers.B = 0x123456
        self.registers.S = 0xABCDEF
        self.registers.T = 0x654321
        self.registers.F = 0x112233445566

        self.assertEqual(self.registers.B, 0x123456)
        self.assertEqual(self.registers.S, 0xABCDEF)
        self.assertEqual(self.registers.T, 0x654321)
        self.assertEqual(self.registers.F, 0x112233445566)

    def test_truncation_xe_registers(self):
        """
        Verifies that SIC/XE registers truncate values to their respective bit widths.
        B, S, T: 24 bits
        F: 48 bits
        """
        # B, S, T are 24-bit registers
        self.registers.B = 0x99123456  # 32-bit value
        self.assertEqual(self.registers.B, 0x123456, "Register B should be truncated to 24 bits.")

        self.registers.S = 0xFFABCDEF
        self.assertEqual(self.registers.S, 0xABCDEF, "Register S should be truncated to 24 bits.")

        self.registers.T = 0xAA654321
        self.assertEqual(self.registers.T, 0x654321, "Register T should be truncated to 24 bits.")

        # F is a 48-bit register
        self.registers.F = 0xFF112233445566  # 56-bit value (top byte FF should be truncated)
        self.assertEqual(self.registers.F, 0x112233445566, "Register F should be truncated to 48 bits.")

if __name__ == '__main__':
    unittest.main()
