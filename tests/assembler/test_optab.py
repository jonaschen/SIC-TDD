import unittest
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.assembler.optab import OpcodeTable

class TestOpcodeTable(unittest.TestCase):
    """
    Test suite for the Opcode Table (OPTAB).
    """

    def setUp(self):
        self.optab = OpcodeTable()

    def test_lookup_existing_opcode(self):
        """
        Tests that valid mnemonics return the correct opcode.
        """
        self.assertEqual(self.optab.get_opcode("LDA"), 0x00)
        self.assertEqual(self.optab.get_opcode("STA"), 0x0C)
        self.assertEqual(self.optab.get_opcode("JEQ"), 0x30)

    def test_lookup_non_existent_opcode(self):
        """
        Tests that looking up an invalid mnemonic raises a KeyError.
        """
        with self.assertRaises(KeyError):
            self.optab.get_opcode("INVALID")

    def test_is_mnemonic_true(self):
        """
        Tests that is_mnemonic returns True for a valid mnemonic.
        """
        self.assertTrue(self.optab.is_mnemonic("ADD"))
        self.assertTrue(self.optab.is_mnemonic("COMP"))

    def test_is_mnemonic_false(self):
        """
        Tests that is_mnemonic returns False for an invalid mnemonic.
        """
        self.assertFalse(self.optab.is_mnemonic("SUBTRACT"))
        self.assertFalse(self.optab.is_mnemonic("JUMP"))

if __name__ == '__main__':
    unittest.main()
