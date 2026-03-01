import unittest
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.cpu import CPU
from src.memory import Memory
from src.registers import Registers
from src.machine import SICMachine

class MockDevice:
    def __init__(self, ready=True):
        self.ready = ready
        self.read_data = []
        self.written_data = []

    def test(self) -> bool:
        return self.ready

    def read(self) -> int:
        return self.read_data.pop(0) if self.read_data else 0

    def write(self, value: int):
        self.written_data.append(value)

    def reset(self):
        self.read_data = []
        self.written_data = []

class TestIO(unittest.TestCase):
    def setUp(self):
        self.machine = SICMachine()
        self.cpu = self.machine.cpu
        self.memory = self.machine.memory
        self.registers = self.machine.registers

    def test_td_instruction_ready(self):
        # Setup device ID 0xF1 as a ready device
        device = MockDevice(ready=True)
        self.machine.device_manager.add_device(0xF1, device)

        # Instruction TD 0xF1 (Opcode 0xE0, Address 0xF1)
        self.memory.write_word(0x2000, 0xE000F1)
        self.registers.PC = 0x2000

        self.cpu.step()

        self.assertEqual(self.registers.SW, ord('<'), "SW should be '<' when device is ready")

    def test_td_instruction_busy(self):
        device = MockDevice(ready=False)
        self.machine.device_manager.add_device(0xF2, device)

        # Instruction TD 0xF2
        self.memory.write_word(0x2000, 0xE000F2)
        self.registers.PC = 0x2000

        self.cpu.step()

        self.assertEqual(self.registers.SW, ord('='), "SW should be '=' when device is busy")

    def test_rd_instruction(self):
        device = MockDevice()
        device.read_data = [0xAB]
        self.machine.device_manager.add_device(0xF3, device)

        # Instruction RD 0xF3
        self.memory.write_word(0x2000, 0xD800F3)
        self.registers.PC = 0x2000
        self.registers.A = 0x123456

        self.cpu.step()

        # A register is 24-bit. RD replaces only the rightmost 8 bits.
        self.assertEqual(self.registers.A, 0x1234AB, "Register A should contain 0xAB in low 8 bits")

    def test_wd_instruction(self):
        device = MockDevice()
        self.machine.device_manager.add_device(0xF4, device)

        # Instruction WD 0xF4
        self.memory.write_word(0x2000, 0xDC00F4)
        self.registers.PC = 0x2000
        self.registers.A = 0x1234CD

        self.cpu.step()

        self.assertEqual(device.written_data, [0xCD], "Device should have received 0xCD")

    def test_console_input_device(self):
        from src.devices import ConsoleInputDevice
        dev = ConsoleInputDevice()
        dev.set_input("HELLO")
        self.assertTrue(dev.test())
        self.assertEqual(dev.read(), ord('H'))
        self.assertEqual(dev.read(), ord('E'))

    def test_console_output_device(self):
        from src.devices import ConsoleOutputDevice
        dev = ConsoleOutputDevice()
        dev.write(ord('A'))
        dev.write(ord('B'))
        self.assertEqual(dev.get_output(), "AB")

    def test_disk_device(self):
        from src.devices import DiskDevice
        # Simple simulation: DiskDevice behaves like a stream for now
        dev = DiskDevice()
        dev.write(0xDE)
        dev.write(0xAD)
        # Assuming we can seek or it's just a buffer
        dev.seek(0)
        self.assertEqual(dev.read(), 0xDE)
        self.assertEqual(dev.read(), 0xAD)

    def test_tape_device(self):
        from src.devices import TapeDevice
        dev = TapeDevice()
        dev.write(0xBE)
        dev.write(0xEF)
        dev.rewind()
        self.assertEqual(dev.read(), 0xBE)
        self.assertEqual(dev.read(), 0xEF)

    def test_console_input_device_reset(self):
        from src.devices import ConsoleInputDevice
        dev = ConsoleInputDevice()
        dev.set_input("TEST")
        self.assertTrue(dev.test())
        self.assertEqual(dev.read(), ord('T'))

        dev.reset()
        self.assertFalse(dev.test())
        self.assertEqual(dev.read(), 0)

    def test_console_output_device_reset(self):
        from src.devices import ConsoleOutputDevice
        dev = ConsoleOutputDevice()
        dev.write(ord('A'))
        self.assertEqual(dev.get_output(), "A")

        dev.reset()
        self.assertEqual(dev.get_output(), "")

    def test_file_backed_device_reset(self):
        from src.devices import FileBackedDevice
        dev = FileBackedDevice()
        dev.write(0xFF)
        dev.seek(0)
        self.assertEqual(dev.read(), 0xFF)

        dev.reset()
        dev.seek(0)
        self.assertEqual(dev.read(), 0)

    def test_device_manager_reset(self):
        device1 = MockDevice()
        device1.write(0x12)

        device2 = MockDevice()
        device2.write(0x34)

        self.machine.device_manager.add_device(0x10, device1)
        self.machine.device_manager.add_device(0x20, device2)

        self.assertEqual(device1.written_data, [0x12])
        self.assertEqual(device2.written_data, [0x34])

        self.machine.device_manager.reset()

        self.assertEqual(device1.written_data, [])
        self.assertEqual(device2.written_data, [])

if __name__ == '__main__':
    unittest.main()
