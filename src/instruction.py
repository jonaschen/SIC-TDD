class Instruction:
    """
    Represents a single SIC/XE instruction, decoded from a 24-bit word.
    This class handles parsing of the standard SIC format (Format 3).
    """

    def __init__(self, word: int):
        """
        Decodes a 24-bit instruction word.
        
        Args:
            word (int): The 24-bit integer representing the machine instruction.
        """
        if not (0 <= word <= 0xFFFFFF):
            raise ValueError("Instruction word must be a 24-bit value.")
        
        self._word = word
        # The properties below will perform the decoding on demand.

    @property
    def opcode(self) -> int:
        """
        Returns the 8-bit opcode of the instruction.
        The opcode is the most significant 8 bits.
        """
        return self._word >> 16

    @property
    def x(self) -> int:
        """
        Returns the indexing bit (X). 1 if indexed, 0 otherwise.
        This is bit 15 of the instruction word.
        """
        return (self._word >> 15) & 1

    @property
    def address(self) -> int:
        """
        Returns the 15-bit address part of the instruction.
        This corresponds to bits 0-14.
        """
        return self._word & 0x7FFF

