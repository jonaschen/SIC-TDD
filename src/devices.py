import io

class IODevice:
    """
    Abstract base class for all Input/Output devices in the SIC emulator.
    """
    def test(self) -> bool:
        """Returns True if the device is ready, False if busy."""
        return True

    def reset(self):
        """Resets the device to its initial state."""
        pass

    def read(self) -> int:
        """Reads a single byte from the device."""
        return 0

    def write(self, value: int):
        """Writes a single byte to the device."""
        pass

class ConsoleInputDevice(IODevice):
    """
    Simulates terminal input.
    """
    def __init__(self):
        self._buffer = []

    def set_input(self, data: str):
        """Pre-loads the input buffer with a string."""
        self._buffer.extend([ord(c) for c in data])

    def test(self) -> bool:
        """Ready if there is data in the buffer."""
        return len(self._buffer) > 0

    def reset(self):
        """Clears the input buffer."""
        self._buffer = []

    def read(self) -> int:
        """Reads the next byte from the buffer."""
        if self._buffer:
            return self._buffer.pop(0)
        return 0

class ConsoleOutputDevice(IODevice):
    """
    Simulates terminal output.
    """
    def __init__(self):
        self._output = []

    def write(self, value: int):
        """Writes a byte (as a character) to the output buffer."""
        self._output.append(chr(value & 0xFF))

    def reset(self):
        """Clears the output buffer."""
        self._output = []

    def get_output(self) -> str:
        """Returns the accumulated output as a string."""
        return "".join(self._output)

class FileBackedDevice(IODevice):
    """
    Base class for devices that are backed by a byte stream.
    Used for Disk and Tape simulations.
    """
    def __init__(self):
        self._stream = io.BytesIO()

    def reset(self):
        """Resets the stream to an empty state."""
        self._stream = io.BytesIO()

    def read(self) -> int:
        """Reads a single byte from the stream."""
        byte = self._stream.read(1)
        if not byte:
            return 0
        return byte[0]

    def write(self, value: int):
        """Writes a single byte to the stream."""
        self._stream.write(bytes([value & 0xFF]))

    def seek(self, offset: int):
        """Seeks to a specific position in the stream."""
        self._stream.seek(offset)

class DiskDevice(FileBackedDevice):
    """
    Simulates a Disk device.
    """
    pass

class TapeDevice(FileBackedDevice):
    """
    Simulates a Tape device.
    """
    def rewind(self):
        """Rewinds the tape to the beginning."""
        self.seek(0)

class DeviceManager:
    """
    Manages the collection of IO devices attached to the SIC machine.
    """
    def __init__(self):
        self._devices = {}

    def add_device(self, device_id: int, device: IODevice):
        """Registers a device with a given 8-bit ID."""
        self._devices[device_id & 0xFF] = device

    def reset(self):
        """Resets all registered devices."""
        for device in self._devices.values():
            device.reset()

    def get_device(self, device_id: int) -> IODevice:
        """Retrieves the device associated with the given ID, or None if not found."""
        return self._devices.get(device_id & 0xFF)
