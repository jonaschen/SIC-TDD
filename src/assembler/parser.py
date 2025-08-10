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
        # A simple split by whitespace is sufficient for the standard format.
        # This is robust enough to handle variable spacing between components.
        parts = line.split()
        
        if len(parts) == 3:
            return parts[0], parts[1], parts[2]
        
        # This is a placeholder for more complex parsing logic to come,
        # such as handling lines without labels or operands.
        # For now, we only handle the full line case.
        return None, None, None
