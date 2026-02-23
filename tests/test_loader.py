import unittest
from src.machine import SICMachine
from src.loader import Loader

class TestLoader(unittest.TestCase):
    def setUp(self):
        self.machine = SICMachine()
        self.loader = Loader(self.machine)

    def test_load_header_record(self):
        # H^COPY  ^001000^00107A
        # Note: In standard SIC, names are 6 chars, addresses 6 hex digits
        obj_code = "HCOPY  00100000107A"
        # For now, just ensuring it doesn't crash and maybe stores metadata if we want
        self.loader.load(obj_code)
        # Check if some internal state is updated or if it just moves on
        # Probably nothing to check in memory yet

    def test_load_text_record(self):
        # H record is usually required first to set context
        # T^001000^02^001003
        # T, then 6 digits address, 2 digits length, then hex pairs
        obj_code = "HCOPY  00100000107A\nT00100003001003"
        self.loader.load(obj_code)

        # Address 001000 should have 001003
        val = self.machine.memory.read_word(0x1000)
        self.assertEqual(val, 0x001003)

    def test_load_end_record(self):
        # E^001000
        obj_code = "HCOPY  00100000107A\nT00100003001003\nE001000"
        self.loader.load(obj_code)

        # PC should be set to 0x1000
        self.assertEqual(self.machine.registers.PC, 0x1000)

    def test_multiple_text_records(self):
        obj_code = (
            "HCOPY  00100000107A\n"
            "T00100003001003\n"
            "T00100303001006\n"
            "E001000"
        )
        self.loader.load(obj_code)
        self.assertEqual(self.machine.memory.read_word(0x1000), 0x001003)
        self.assertEqual(self.machine.memory.read_word(0x1003), 0x001006)
        self.assertEqual(self.machine.registers.PC, 0x1000)

    def test_relocation_record(self):
        # M^001001^04+COPY
        # This is more advanced. SIC/XE relocation.
        # M, then 6 digits start addr, 2 digits length (half-bytes), flag, symbol
        # For absolute loader, relocation might be added to a base load address.

        # Let's say we load at 0x2000 instead of 0x1000
        obj_code = (
            "HCOPY  00000000107A\n" # Program starts at 0 relative
            "T00000003000003\n"     # Word at 000000 is 000003 (address to be relocated)
            "M00000006+COPY\n"      # Relocate 6 half-bytes (3 bytes) at addr 0
            "E000000"
        )
        # Load at 0x2000
        self.loader.load(obj_code, load_address=0x2000)

        # The word at 0x2000 should be 0x000003 + 0x2000 = 0x002003
        self.assertEqual(self.machine.memory.read_word(0x2000), 0x2003)
        # PC should be 0x2000
        self.assertEqual(self.machine.registers.PC, 0x2000)

    def test_relocation_record_format4(self):
        # Format 4 instruction: +JSUB RDREC (48 10 10 36 in hex, if RDREC is at 0x1036)
        # If RDREC is relative to program start (0), and we load at 0x2000.
        # Record: T0000010448100000  (assuming JSUB is at 0001, address field is 00000)
        # Modification record: M00000205+COPY (modify 5 half-bytes starting at 0002)

        obj_code = (
            "HCOPY  00000000107A\n"
            "T0000010448100000\n" # JSUB at addr 1, 4 bytes long. Byte 1 is 48, Byte 2 is 10, Byte 3 & 4 are 00 00.
                                  # The 20-bit address starts at Byte 2's last 4 bits.
                                  # Wait, 48 is Byte 0. 10 is Byte 1. 00 is Byte 2. 00 is Byte 3.
                                  # Field to modify starts at address + 1 = 2.
                                  # Wait, address + 1 is Byte 1.
                                  # Byte 0: 48
                                  # Byte 1: 10
                                  # Byte 2: 00
                                  # Byte 3: 00
                                  # 20 bit address is in Byte 1 (last 4 bits), Byte 2, Byte 3.
                                  # So M00000205 means it starts at Byte 1.
            "M00000205+COPY\n"
            "E000000"
        )

        # In our memory:
        # Address 1: 48
        # Address 2: 10
        # Address 3: 00
        # Address 4: 00

        self.loader.load(obj_code, load_address=0x2000)

        # After relocation at 0x2000:
        # Addresses in memory are 0x2001, 0x2002, 0x2003, 0x2004.
        # Original values: 0x48, 0x10, 0x00, 0x00
        # Relocation at 0x2002 (target_address = 0x0002 + 0x2000 = 0x2002)
        # Read 3 bytes from 0x2002: 10, 00, 00 -> 0x100000
        # Add 0x2000 to last 20 bits (0x00000): 0x00000 + 0x2000 = 0x02000
        # Combine back: 0x100000 | 0x02000 = 0x102000
        # Write back to 0x2002: 10, 20, 00

        self.assertEqual(self.machine.memory.read_byte(0x2001), 0x48)
        self.assertEqual(self.machine.memory.read_byte(0x2002), 0x10)
        self.assertEqual(self.machine.memory.read_byte(0x2003), 0x20)
        self.assertEqual(self.machine.memory.read_byte(0x2004), 0x00)

if __name__ == '__main__':
    unittest.main()
