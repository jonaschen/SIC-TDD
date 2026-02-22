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
        # Handle empty lines and comments (though PassOne might filter them too)
        if not line or not line.strip() or line.strip().startswith('.'):
            return None, None, None

        parts = line.split()
        if not parts:
            return None, None, None

        label = None
        mnemonic = None
        operand = None

        # Check if there is a label (line does not start with whitespace)
        # Note: We use the original line string to check indentation
        has_label = not line[0].isspace()
        
        idx = 0
        if has_label:
            if idx < len(parts):
                label = parts[idx]
                idx += 1
        
        if idx < len(parts):
            mnemonic = parts[idx]
            idx += 1

        if idx < len(parts):
            operand = parts[idx]
            idx += 1

        return label, mnemonic, operand
