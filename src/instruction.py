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
        # Decoding logic to be implemented.

    @property
    def opcode(self) -> int:
        """
        Returns the 8-bit opcode of the instruction.
        """
        raise NotImplementedError

    @property
    def x(self) -> int:
        """
        Returns the indexing bit (X). 1 if indexed, 0 otherwise.
        """
        raise NotImplementedError

    @property
    def address(self) -> int:
        """
        Returns the 15-bit address part of the instruction.
        """
        raise NotImplementedError

