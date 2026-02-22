from .parser import LineParser
from .optab import OpcodeTable
from .symtab import SymbolTable
from .directive_handlers import (
    WordDirectiveHandler, ReswDirectiveHandler, 
    ResbDirectiveHandler, ByteDirectiveHandler
)

class PassOneResult:
    def __init__(self, program_length, execution_start_address):
        self.program_length = program_length
        self.execution_start_address = execution_start_address

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

    def run(self, source_lines: list[str]) -> tuple[SymbolTable, PassOneResult]:
        """
        Executes Pass One of the assembler.

        Args:
            source_lines: A list of strings, where each string is a line of source code.

        Returns:
            A tuple containing the populated SymbolTable and a result object with program length.
        """
        symtab = SymbolTable()
        locctr = 0
        start_address = 0
        execution_start_address = 0

        # Pre-process lines to handle START directive correctly
        # We need to find the first real instruction/directive
        processed_lines = []
        for line in source_lines:
            if line.strip() and not line.strip().startswith('.'):
                processed_lines.append(line)

        if not processed_lines:
             return symtab, PassOneResult(0, 0)

        # check first line for START
        first_line = processed_lines[0]
        label, mnemonic, operand = self.parser.parse(first_line)

        if mnemonic == 'START':
            start_address = int(operand, 16) if operand else 0
            locctr = start_address
            execution_start_address = start_address
            if label:
                symtab.add_symbol(label, locctr)
            processed_lines = processed_lines[1:]
        else:
            start_address = 0
            locctr = 0
            execution_start_address = 0
        
        for line in processed_lines:
            label, mnemonic, operand = self.parser.parse(line)

            if mnemonic == 'END':
                if operand:
                    # Try to resolve operand as symbol or hex
                    if symtab.has_symbol(operand):
                        execution_start_address = symtab.get_address(operand)
                    else:
                        try:
                            execution_start_address = int(operand, 16)
                        except ValueError:
                            pass # Keep default
                break

            if label:
                if symtab.has_symbol(label):
                     raise ValueError(f"Duplicate symbol found: {label}")
                symtab.add_symbol(label, locctr)

            if not mnemonic:
                continue

            if self.optab.is_mnemonic(mnemonic):
                locctr += 3
            elif mnemonic in self.directive_handlers:
                handler = self.directive_handlers[mnemonic]
                locctr += handler.handle(operand)
            else:
                raise ValueError(f"Invalid operation code: {mnemonic}")

        program_length = locctr - start_address
        return symtab, PassOneResult(program_length, execution_start_address)
