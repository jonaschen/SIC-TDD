class Instruction:
    """
    Represents a single SIC/XE instruction, decoded from a machine word.
    This class handles parsing of Format 2 (16-bit) and Format 3 (24-bit) instructions.
    """

    def __init__(self, word: int, format: int = 3):
        """
        Decodes an instruction word.
        
        Args:
            word (int): The integer representing the machine instruction.
            format (int): The instruction format (2 or 3).
        """
        self._word = word
        self._format = format

    @property
    def format(self) -> int:
        return self._format

    @property
    def opcode(self) -> int:
        """
        Returns the 8-bit opcode of the instruction.
        """
        if self._format == 2:
            return (self._word >> 8) & 0xFF
        return (self._word >> 16) & 0xFF

    @property
    def x(self) -> int:
        """
        Returns the indexing bit (X). 1 if indexed, 0 otherwise.
        This is bit 15 of a 24-bit instruction word (Format 3).
        """
        if self._format != 3:
            return 0
        return (self._word >> 15) & 1

    @property
    def address(self) -> int:
        """
        Returns the 15-bit address part of a Format 3 instruction.
        This corresponds to bits 0-14.
        """
        if self._format != 3:
            return 0
        return self._word & 0x7FFF

    @property
    def r1(self) -> int:
        """
        Returns the first register operand (r1) for Format 2 instructions.
        """
        if self._format != 2:
            return 0
        return (self._word >> 4) & 0xF

    @property
    def r2(self) -> int:
        """
        Returns the second register operand (r2) for Format 2 instructions.
        """
        if self._format != 2:
            return 0
        return self._word & 0xF
