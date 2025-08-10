class SymbolTable:
    """
    Represents the Symbol Table (SYMTAB) for the SIC assembler.
    It stores a mapping of label names to their memory addresses.
    """

    def __init__(self):
        """
        Initializes an empty SYMTAB.
        """
        # To be implemented
        pass

    def add_symbol(self, label: str, address: int):
        """
        Adds a new symbol and its address to the table.

        Args:
            label: The symbol's name.
            address: The symbol's memory address.

        Raises:
            ValueError: If the symbol already exists in the table.
        """
        raise NotImplementedError

    def has_symbol(self, label: str) -> bool:
        """
        Checks if a symbol exists in the table.

        Args:
            label: The symbol to check.

        Returns:
            True if the symbol exists, False otherwise.
        """
        raise NotImplementedError

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
        raise NotImplementedError
