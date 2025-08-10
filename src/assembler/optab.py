class OpcodeTable:
    """
    Represents the Opcode Table (OPTAB) for the SIC machine.
    It stores a mapping of mnemonic names to their machine code values.
    """

    def __init__(self):
        """
        Initializes the OPTAB with all the standard SIC instructions.
        """
        # To be implemented
        pass

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
        raise NotImplementedError

    def is_mnemonic(self, mnemonic: str) -> bool:
        """
        Checks if a mnemonic exists in the OPTAB.

        Args:
            mnemonic: The mnemonic to check.

        Returns:
            True if the mnemonic is valid, False otherwise.
        """
        raise NotImplementedError
