import unittest
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.instruction import Instruction

class TestInstruction(unittest.TestCase):
    """
    Test suite for the Instruction decoding logic.
    """

    def test_decode_format3_instruction(self):
        """
        Tests the decoding of a standard SIC Format 3 instruction.
        The instruction word represents 'STA 0x2000,X'
        Opcode for STA is 0x0C.
        Address is 0x2000.
        Indexing (X bit) is 1.
        
        The resulting 24-bit word is:
        Opcode (8 bits) | X (1 bit) | Address (15 bits)
        00001100        | 1         | 010000000000000
        Which is 0x0C_A000 in hexadecimal.
        """
        instruction_word = 0x0CA000
        
        instr = Instruction(instruction_word)

        # Verify the decoded components
        self.assertEqual(instr.opcode, 0x0C, "Opcode should be decoded correctly.")
        self.assertEqual(instr.x, 1, "Indexing bit (X) should be decoded correctly.")
        self.assertEqual(instr.address, 0x2000, "Address should be decoded correctly.")

    def test_decode_instruction_without_indexing(self):
        """
        Tests the decoding of a standard SIC instruction without indexing.
        The instruction word represents 'LDA 0x1000'
        Opcode for LDA is 0x00.
        Address is 0x1000.
        Indexing (X bit) is 0.
        
        The resulting 24-bit word is 0x001000.
        """
        instruction_word = 0x001000

        instr = Instruction(instruction_word)

        # Verify the decoded components
        self.assertEqual(instr.opcode, 0x00, "Opcode should be decoded correctly.")
        self.assertEqual(instr.x, 0, "Indexing bit (X) should be 0.")
        self.assertEqual(instr.address, 0x1000, "Address should be decoded correctly.")


if __name__ == '__main__':
    unittest.main()