import unittest
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.assembler.pass_one import PassOne

class TestPassOne(unittest.TestCase):
    """
    Test suite for Pass One of the SIC Assembler.
    """

    def setUp(self):
        self.pass_one = PassOne()

    def test_run_pass_one_on_simple_program(self):
        """
        Tests that Pass One correctly processes a simple program,
        generating the correct symbol table and program length.
        """
        source_code = [
            "COPY    START   1000",
            "FIRST   LDA     FIVE",
            "        STA     ALPHA",
            "FIVE    WORD    5",
            "ALPHA   RESW    1",
            "        END     FIRST"
        ]

        symtab, program_length = self.pass_one.run(source_code)

        # Verify the program length
        # 1000 -> 1003 (LDA) -> 1006 (STA) -> 1009 (WORD) -> 100C (RESW)
        # Length = 100C - 1000 = C (or 12 in decimal)
        self.assertEqual(program_length, 12)

        # Verify the symbol table
        self.assertEqual(symtab.get_address("COPY"), 0x1000)
        self.assertEqual(symtab.get_address("FIRST"), 0x1000)
        self.assertEqual(symtab.get_address("FIVE"), 0x1006)
        self.assertEqual(symtab.get_address("ALPHA"), 0x1009)
        self.assertFalse(symtab.has_symbol("END")) # END is a directive, not a label

    def test_missing_start_directive_defaults_to_zero(self):
        """
        Tests that a program without a START directive defaults to address 0.
        """
        source = [
            "FIRST   STL     RETADR",
            "RETADR  RESW    1",
            "        END     FIRST"
        ]
        symtab, program_length = self.pass_one.run(source)
        self.assertEqual(program_length, 6)
        self.assertEqual(symtab.get_address("FIRST"), 0x0000)
        self.assertEqual(symtab.get_address("RETADR"), 0x0003)

    def test_duplicate_symbol_raises_error(self):
        """
        Tests that a duplicate symbol in the source code raises a ValueError.
        """
        source = [
            "COPY    START   1000",
            "FIRST   STL     RETADR",
            "FIRST   LDA     ALPHA",
            "        END     FIRST"
        ]
        with self.assertRaisesRegex(ValueError, "Duplicate symbol found: FIRST"):
            self.pass_one.run(source)
            
    def test_handles_comment_lines(self):
        """
        Tests that comment lines (starting with '.') are ignored correctly.
        """
        source_code = [
            "COPY    START   2000",
            ". THIS IS A COMMENT, SHOULD BE IGNORED",
            "FIRST   LDA     BETA",
            "BETA    RESW    1",
            "        END     COPY"
        ]
        symtab, program_length = self.pass_one.run(source_code)
        
        # Length should be 6 (3 bytes for LDA, 3 for RESW 1)
        self.assertEqual(program_length, 6)
        self.assertTrue(symtab.has_symbol("FIRST"))
        self.assertEqual(symtab.get_address("FIRST"), 0x2000)
        self.assertEqual(symtab.get_address("BETA"), 0x2003)


if __name__ == '__main__':
    unittest.main()
