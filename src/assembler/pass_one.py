from .parser import LineParser
from .optab import OpcodeTable
from .symtab import SymbolTable

class PassOne:
    """
    Implements Pass One of the SIC assembler.
    This pass reads the source code, builds the symbol table (SYMTAB),
    and calculates the program length.
    """

    def __init__(self):
        self.parser = LineParser()
        self.optab = OpcodeTable()

    def run(self, source_lines: list[str]) -> tuple[SymbolTable, int]:
        """
        Executes Pass One of the assembler.

        Args:
            source_lines: A list of strings, where each string is a line of source code.

        Returns:
            A tuple containing the populated SymbolTable and the total program length in bytes.
        """
        # To be implemented
        raise NotImplementedError
