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

if __name__ == '__main__':
    unittest.main()