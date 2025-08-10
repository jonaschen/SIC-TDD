class SymbolTable:
    """
    Represents the Symbol Table (SYMTAB) for the SIC assembler.
    It stores a mapping of label names to their memory addresses.
    """

    def __init__(self):
        """
        Initializes an empty SYMTAB.
        """
        self._symbols = {}

    def add_symbol(self, label: str, address: int):
        """
        Adds a new symbol and its address to the table.

        Args:
            label: The symbol's name.
            address: The symbol's memory address.

        Raises:
            ValueError: If the symbol already exists in the table.
        """
        label_upper = label.upper()
        if label_upper in self._symbols:
            raise ValueError(f"Duplicate symbol found: {label}")
        self._symbols[label_upper] = address

    def has_symbol(self, label: str) -> bool:
        """
        Checks if a symbol exists in the table.

        Args:
            label: The symbol to check.

        Returns:
            True if the symbol exists, False otherwise.
        """
        return label.upper() in self._symbols

    def get_address(self, label: str) -> int:
        """
        Retrieves the address of a given symbol.

        Args:
            label: The symbol whose address is to be retrieved.

        Returns:
            The integer address of the symbol.

        Raises:
            KeyError: If the symbol does not exist.
        """
        return self._symbols[label.upper()]
