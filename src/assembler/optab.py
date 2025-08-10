class OpcodeTable:
    """
    Represents the Opcode Table (OPTAB) for the SIC machine.
    It stores a mapping of mnemonic names to their machine code values.
    """

    def __init__(self):
        """
        Initializes the OPTAB with all the standard SIC instructions.
        """
        self._opcodes = {
            "ADD": 0x18, "AND": 0x40, "COMP": 0x28, "DIV": 0x24,
            "J": 0x3C, "JEQ": 0x30, "JGT": 0x34, "JLT": 0x38,
            "JSUB": 0x48, "LDA": 0x00, "LDCH": 0x50, "LDL": 0x08,
            "LDX": 0x04, "MUL": 0x20, "OR": 0x44, "RD": 0xD8,
            "RSUB": 0x4C, "STA": 0x0C, "STCH": 0x54, "STL": 0x14,
            "STSW": 0xE8, "STX": 0x10, "SUB": 0x1C, "TD": 0xE0,
            "TIX": 0x2C, "WD": 0xDC
        }

    def get_opcode(self, mnemonic: str) -> int:
        """
        Looks up the machine code for a given mnemonic.

        Args:
            mnemonic: The instruction mnemonic (e.g., "LDA").

        Returns:
            The integer opcode.

        Raises:
            KeyError: If the mnemonic does not exist in the table.
        """
        return self._opcodes[mnemonic.upper()]

    def is_mnemonic(self, mnemonic: str) -> bool:
        """
        Checks if a mnemonic exists in the OPTAB.

        Args:
            mnemonic: The mnemonic to check.

        Returns:
            True if the mnemonic is valid, False otherwise.
        """
        return mnemonic.upper() in self._opcodes
