import unittest
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.assembler.directive_handlers import (
    WordDirectiveHandler,
    ReswDirectiveHandler,
    ResbDirectiveHandler,
    ByteDirectiveHandler,
)

class TestWordDirectiveHandler(unittest.TestCase):
    def setUp(self):
        self.handler = WordDirectiveHandler()

    def test_handle_valid_operand(self):
        self.assertEqual(self.handler.handle("10"), 3)

    def test_handle_none_operand(self):
        self.assertEqual(self.handler.handle(None), 3)

class TestReswDirectiveHandler(unittest.TestCase):
    def setUp(self):
        self.handler = ReswDirectiveHandler()

    def test_handle_valid_operand(self):
        self.assertEqual(self.handler.handle("10"), 30)

    def test_handle_none_operand(self):
        with self.assertRaisesRegex(ValueError, "RESW requires an operand."):
            self.handler.handle(None)

    def test_handle_invalid_operand(self):
        with self.assertRaises(ValueError):
            self.handler.handle("abc")

class TestResbDirectiveHandler(unittest.TestCase):
    def setUp(self):
        self.handler = ResbDirectiveHandler()

    def test_handle_valid_operand(self):
        self.assertEqual(self.handler.handle("10"), 10)

    def test_handle_none_operand(self):
        with self.assertRaisesRegex(ValueError, "RESB requires an operand."):
            self.handler.handle(None)

    def test_handle_invalid_operand(self):
        with self.assertRaises(ValueError):
            self.handler.handle("abc")

class TestByteDirectiveHandler(unittest.TestCase):
    def setUp(self):
        self.handler = ByteDirectiveHandler()

    def test_handle_char_string(self):
        self.assertEqual(self.handler.handle("C'EOF'"), 3)

    def test_handle_hex_string(self):
        self.assertEqual(self.handler.handle("X'F1'"), 1)
        self.assertEqual(self.handler.handle("X'0A0B'"), 2)

    def test_handle_lowercase_prefix(self):
        self.assertEqual(self.handler.handle("c'abc'"), 3)
        self.assertEqual(self.handler.handle("x'ff'"), 1)

    def test_handle_none_operand(self):
        with self.assertRaisesRegex(ValueError, "BYTE requires an operand."):
            self.handler.handle(None)

    def test_handle_invalid_format(self):
        with self.assertRaisesRegex(ValueError, "Invalid BYTE operand format: Z'123'"):
            self.handler.handle("Z'123'")

if __name__ == '__main__':
    unittest.main()
