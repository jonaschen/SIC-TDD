class Memory:
    """
    Represents the 32K byte-addressable memory of the SIC/XE machine.
    A SIC word is 24 bits (3 bytes).
    """
    
    # SIC memory size is 32,768 bytes (2^15)
    SIZE = 32768

    def __init__(self):
        """
        Initializes the memory. All bytes are set to 0.
        """
        # A bytearray is a mutable sequence of integers in the range 0 <= x < 256.
        # It's an efficient way to represent a block of memory.
        self._memory = bytearray(self.SIZE)

    def read_byte(self, address):
        """
        Reads a single byte from the specified address.
        
        Args:
            address (int): The address from which to read the byte.
            
        Returns:
            int: The byte value at the given address.
            
        Raises:
            IndexError: If the address is out of bounds.
        """
        if not (0 <= address < self.SIZE):
            raise IndexError(f"Address {address} is out of bounds for memory size {self.SIZE}.")
        
        return self._memory[address]


    def write_byte(self, address, value):
        """
        Writes a single byte to the specified address.
        Values larger than 8 bits will be truncated.
        
        Args:
            address (int): The address where the byte will be written.
            value (int): The byte value to write.
            
        Raises:
            IndexError: If the address is out of bounds.
        """
        if not (0 <= address < self.SIZE):
            raise IndexError(f"Address {address} is out of bounds for memory size {self.SIZE}.")
        
        # Mask the value to ensure it's a single byte (8 bits).
        # This handles Test 10.
        self._memory[address] = value & 0xFF

    def read_word(self, address):
        """
        Reads a 24-bit word (3 bytes) starting from the specified address.
        Words are stored in big-endian format.
        
        Args:
            address (int): The starting address of the word.
            
        Returns:
            int: The 24-bit word value.
            
        Raises:
            IndexError: If the address or the subsequent bytes are out of bounds.
        """
        # To be implemented
        raise NotImplementedError("read_word not implemented yet")

    def write_word(self, address, value):
        """
        Writes a 24-bit word (3 bytes) starting at the specified address.
        The value is stored in big-endian format.
        Values larger than 24 bits will be truncated.
        
        Args:
            address (int): The starting address for the word.
            value (int): The 24-bit value to write.
            
        Raises:
            IndexError: If the address or the subsequent bytes are out of bounds.
        """
        # To be implemented
        raise NotImplementedError("write_word not implemented yet")

