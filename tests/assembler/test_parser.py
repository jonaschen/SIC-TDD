import unittest
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.assembler.parser import LineParser

class TestLineParser(unittest.TestCase):
    """
    Test suite for the assembly line parser.
    """

    def setUp(self):
        self.parser = LineParser()

    def test_parse_full_line(self):
        """
        Tests parsing a standard line with a label, mnemonic, and operand.
        """
        line = "LOOP   STA   BUFFER,X"
        label, mnemonic, operand = self.parser.parse(line)

        self.assertEqual(label, "LOOP")
        self.assertEqual(mnemonic, "STA")
        self.assertEqual(operand, "BUFFER,X")

    def test_parse_empty_line(self):
        """Tests parsing an empty string."""
        label, mnemonic, operand = self.parser.parse("")
        self.assertIsNone(label)
        self.assertIsNone(mnemonic)
        self.assertIsNone(operand)

    def test_parse_whitespace_only(self):
        """Tests parsing a line containing only whitespace."""
        label, mnemonic, operand = self.parser.parse("   \t  ")
        self.assertIsNone(label)
        self.assertIsNone(mnemonic)
        self.assertIsNone(operand)

    def test_parse_comment(self):
        """Tests parsing a comment line starting with '.'"""
        label, mnemonic, operand = self.parser.parse(". This is a comment")
        self.assertIsNone(label)
        self.assertIsNone(mnemonic)
        self.assertIsNone(operand)

    def test_parse_comment_with_leading_whitespace(self):
        """Tests parsing a comment line with leading spaces."""
        label, mnemonic, operand = self.parser.parse("  . Comment")
        self.assertIsNone(label)
        self.assertIsNone(mnemonic)
        self.assertIsNone(operand)

    def test_parse_no_label(self):
        """Tests parsing a line with mnemonic and operand but no label."""
        label, mnemonic, operand = self.parser.parse("  STA BUFFER,X")
        self.assertIsNone(label)
        self.assertEqual(mnemonic, "STA")
        self.assertEqual(operand, "BUFFER,X")

    def test_parse_no_operand(self):
        """Tests parsing a line with label and mnemonic but no operand."""
        label, mnemonic, operand = self.parser.parse("LOOP RSUB")
        self.assertEqual(label, "LOOP")
        self.assertEqual(mnemonic, "RSUB")
        self.assertIsNone(operand)

    def test_parse_mnemonic_only(self):
        """Tests parsing a line with only a mnemonic."""
        label, mnemonic, operand = self.parser.parse("  RSUB")
        self.assertIsNone(label)
        self.assertEqual(mnemonic, "RSUB")
        self.assertIsNone(operand)

    def test_parse_label_only(self):
        """Tests parsing a line with only a label."""
        label, mnemonic, operand = self.parser.parse("LOOP")
        self.assertEqual(label, "LOOP")
        self.assertIsNone(mnemonic)
        self.assertIsNone(operand)

if __name__ == '__main__':
    unittest.main()