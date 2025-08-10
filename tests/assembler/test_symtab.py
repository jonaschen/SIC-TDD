import unittest
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.assembler.symtab import SymbolTable

class TestSymbolTable(unittest.TestCase):
    """
    Test suite for the Symbol Table (SYMTAB).
    """

    def setUp(self):
        self.symtab = SymbolTable()

    def test_add_and_get_symbol(self):
        """
        Tests that a symbol can be added and its address retrieved.
        """
        self.symtab.add_symbol("LOOP", 0x1000)
        self.assertEqual(self.symtab.get_address("LOOP"), 0x1000)

    def test_has_symbol(self):
        """
        Tests the has_symbol method for both existing and non-existing symbols.
        """
        self.symtab.add_symbol("BUFFER", 0x2050)
        self.assertTrue(self.symtab.has_symbol("BUFFER"))
        self.assertFalse(self.symtab.has_symbol("NOT_FOUND"))

    def test_get_non_existent_symbol(self):
        """
        Tests that attempting to get the address of a non-existent symbol raises a KeyError.
        """
        with self.assertRaises(KeyError):
            self.symtab.get_address("UNDEFINED")

    def test_add_duplicate_symbol_raises_error(self):
        """
        Tests that attempting to add a symbol that already exists raises a ValueError.
        """
        self.symtab.add_symbol("DUPE", 0x3000)
        with self.assertRaises(ValueError):
            self.symtab.add_symbol("DUPE", 0x4000)

if __name__ == '__main__':
    unittest.main()
