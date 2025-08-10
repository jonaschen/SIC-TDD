class LineParser:
    """
    Parses a single line of SIC assembly source code into its constituent parts:
    (label, mnemonic, operand).
    """

    def parse(self, line: str) -> tuple[str | None, str | None, str | None]:
        """
        Parses a line of assembly code.

        Args:
            line: A string containing a line of SIC source code.

        Returns:
            A tuple containing the label, mnemonic, and operand.
            If a component is not present, it will be None.
        """
        # To be implemented
        raise NotImplementedError("parse() method not implemented yet.")