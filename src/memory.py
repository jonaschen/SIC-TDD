class Memory:
    def __init__(self, size=0x8000):
        self.size = size
        self._data = None  # Not initialized yet (will cause failures)

    def read_byte(self, address):
        raise NotImplementedError("read_byte not implemented yet")

    def write_byte(self, address, value):
        raise NotImplementedError("write_byte not implemented yet")

    def read_word(self, address):
        raise NotImplementedError("read_word not implemented yet")

    def write_word(self, address, value):
        raise NotImplementedError("write_word not implemented yet")
