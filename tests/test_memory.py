import unittest
import sys
import os

# Add the parent directory to the Python path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.memory import Memory

class TestMemory(unittest.TestCase):
    """
    Test suite for the Memory component of the SIC/XE computer.
    """

    def setUp(self):
        """
        Set up a new Memory instance before each test.
        This ensures that each test runs in isolation.
        """
        self.memory = Memory()

    def test_memory_initialization(self):
        """
        Test 1: Memory should be initialized to all zeros.
        Description: Verifies that every byte in the 32K memory space is 0 upon creation.
        """
        for i in range(self.memory.SIZE):
            self.assertEqual(self.memory.read_byte(i), 0, f"Memory at address {i} should be initialized to 0.")

    def test_write_and_read_byte(self):
        """
        Test 2: Basic byte I/O.
        Description: Verifies that a single byte can be written to and read from an address.
        """
        address = 0x1000
        value = 0x5A
        self.memory.write_byte(address, value)
        self.assertEqual(self.memory.read_byte(address), value, "The byte read should be the same as the byte written.")

    def test_write_and_read_word(self):
        """
        Test 3: Write and read a 3-byte word.
        Description: Verifies that a 24-bit word can be written to and read from memory.
        The word is stored in big-endian format.
        """
        address = 0x2000
        value = 0x123456  # A 24-bit value
        self.memory.write_word(address, value)
        read_value = self.memory.read_word(address)
        self.assertEqual(read_value, value, "The word read should be the same as the word written.")

        # Also verify the individual bytes
        self.assertEqual(self.memory.read_byte(address), 0x12, "High-order byte is incorrect.")
        self.assertEqual(self.memory.read_byte(address + 1), 0x34, "Middle byte is incorrect.")
        self.assertEqual(self.memory.read_byte(address + 2), 0x56, "Low-order byte is incorrect.")

    def test_word_read_write_must_be_3_bytes(self):
        """
        Test 4: Word stores exactly 24 bits.
        Description: Verifies that writing a word only affects three consecutive byte locations.
        """
        address = 0x3000
        value = 0xABCDEF

        # Check bytes before the write
        self.assertEqual(self.memory.read_byte(address - 1), 0)
        self.assertEqual(self.memory.read_byte(address + 3), 0)

        self.memory.write_word(address, value)

        # Check that bytes outside the word are unaffected
        self.assertEqual(self.memory.read_byte(address - 1), 0, "Byte before the word should not be modified.")
        self.assertEqual(self.memory.read_byte(address + 3), 0, "Byte after the word should not be modified.")

    def test_out_of_bounds_byte_access(self):
        """
        Test 5: Byte-level boundary check.
        Description: Verifies that attempting to read or write a byte outside the
        valid memory range raises an exception.
        """
        with self.assertRaises(IndexError, msg="Accessing a negative address should raise an IndexError."):
            self.memory.read_byte(-1)
        with self.assertRaises(IndexError, msg=f"Accessing address {self.memory.SIZE} should raise an IndexError."):
            self.memory.read_byte(self.memory.SIZE)
        with self.assertRaises(IndexError, msg="Writing to a negative address should raise an IndexError."):
            self.memory.write_byte(-1, 0)
        with self.assertRaises(IndexError, msg=f"Writing to address {self.memory.SIZE} should raise an IndexError."):
            self.memory.write_byte(self.memory.SIZE, 0)

    def test_out_of_bounds_word_access(self):
        """
        Test 6: Word-level boundary check.
        Description: Verifies that attempting to read or write a word where any of
        its bytes would fall outside the valid memory range raises an exception.
        """
        # A word write starting at the last possible byte should fail
        with self.assertRaises(IndexError, msg="Writing a word at the end of memory should fail."):
            self.memory.write_word(self.memory.SIZE - 1, 0x123456)
        # A word write starting at the second to last byte should fail
        with self.assertRaises(IndexError, msg="Writing a word at the second to last byte should fail."):
            self.memory.write_word(self.memory.SIZE - 2, 0x123456)
        # A word write starting at the last valid address for a word should succeed
        try:
            self.memory.write_word(self.memory.SIZE - 3, 0x123456)
        except IndexError:
            self.fail("Writing a word at the last valid position should not raise an IndexError.")

    def test_word_masking_behavior(self):
        """
        Test 7: Upper bits are masked out to 24-bit.
        Description: Verifies that if a value larger than 24 bits is passed to write_word,
        it is correctly truncated to 24 bits.
        """
        address = 0x4000
        large_value = 0x99ABCDEF  # 32-bit value
        expected_value = 0xABCDEF  # The lower 24 bits

        self.memory.write_word(address, large_value)
        read_value = self.memory.read_word(address)
        self.assertEqual(read_value, expected_value, "Value should be masked to 24 bits upon writing.")

    def test_write_word_smaller_than_24_bits(self):
        """
        Test 8: Writing a word smaller than 24-bit.
        Description: Ensure values < 0x1000000 are written correctly without shift errors.
        This tests for correct zero-padding of higher-order bytes.
        """
        address = 0x5000
        small_value = 0x123 # A value that fits in 9 bits

        self.memory.write_word(address, small_value)
        read_value = self.memory.read_word(address)

        self.assertEqual(read_value, small_value, "The small word value should be read back correctly.")
        
        # Verify individual bytes to ensure correct big-endian storage with padding
        self.assertEqual(self.memory.read_byte(address), 0x00, "High-order byte should be padded with zero.")
        self.assertEqual(self.memory.read_byte(address + 1), 0x01, "Middle byte is incorrect.")
        self.assertEqual(self.memory.read_byte(address + 2), 0x23, "Low-order byte is incorrect.")

    def test_adjacent_word_writes_no_interference(self):
        """
        Test 9: Adjacent word writes should not interfere.
        Description: Verifies that writing two adjacent words does not corrupt data.
        """
        address1 = 0x6000
        value1 = 0xAAAAAA
        address2 = address1 + 3
        value2 = 0xBBBBBB

        # Write two words next to each other
        self.memory.write_word(address1, value1)
        self.memory.write_word(address2, value2)

        # Verify that the first word is still correct
        self.assertEqual(self.memory.read_word(address1), value1, "The first word was corrupted.")
        # Verify that the second word is correct
        self.assertEqual(self.memory.read_word(address2), value2, "The second word was not written correctly.")

    def test_byte_masking_behavior(self):
        """
        Test 10: Byte masking.
        Description: If a larger-than-8-bit value is written as a byte, it should be truncated.
        """
        address = 0x7000
        large_value = 0x1F4  # This is 500 in decimal, which is larger than 255
        expected_value = 0xF4 # The lower 8 bits

        self.memory.write_byte(address, large_value)
        read_value = self.memory.read_byte(address)
        self.assertEqual(read_value, expected_value, "Value should be masked to 8 bits upon writing.")


if __name__ == '__main__':
    unittest.main()
