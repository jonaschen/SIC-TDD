from .parser import LineParser
from .optab import OpcodeTable
from .symtab import SymbolTable
from .directive_handlers import (
    WordDirectiveHandler, ReswDirectiveHandler, 
    ResbDirectiveHandler, ByteDirectiveHandler
)

class PassOne:
    """
    Implements Pass One of the SIC assembler.
    This pass reads the source code, builds the symbol table (SYMTAB),
    and calculates the program length.
    """

    def __init__(self):
        self.parser = LineParser()
        self.optab = OpcodeTable()
        self.directive_handlers = {
            'WORD': WordDirectiveHandler(),
            'RESW': ReswDirectiveHandler(),
            'RESB': ResbDirectiveHandler(),
            'BYTE': ByteDirectiveHandler(),
        }

    def run(self, source_lines: list[str]) -> tuple[SymbolTable, int]:
        """
        Executes Pass One of the assembler.

        Args:
            source_lines: A list of strings, where each string is a line of source code.

        Returns:
            A tuple containing the populated SymbolTable and the total program length in bytes.
        """
        symtab = SymbolTable()
        locctr = 0
        start_address = 0

        first_line = source_lines[0]
        label, mnemonic, operand = self.parser.parse(first_line)

        if mnemonic == 'START':
            start_address = int(operand, 16) if operand else 0
            locctr = start_address
            if label:
                symtab.add_symbol(label, locctr)
            source_lines = source_lines[1:]
        
        for line in source_lines:
            if line.strip().startswith('.') or not line.strip():
                continue

            label, mnemonic, operand = self.parser.parse(line)

            if mnemonic == 'END':
                break

            if label:
                symtab.add_symbol(label, locctr)

            if self.optab.is_mnemonic(mnemonic):
                locctr += 3
            elif mnemonic in self.directive_handlers:
                handler = self.directive_handlers[mnemonic]
                locctr += handler.handle(operand)
            else:
                raise ValueError(f"Invalid operation code: {mnemonic}")

        program_length = locctr - start_address
        return symtab, program_length
