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
        symtab = SymbolTable()
        locctr = 0
        start_address = 0

        # Handle the START directive on the first line
        first_line = source_lines[0]
        label, mnemonic, operand = self.parser.parse(first_line)

        if mnemonic == 'START':
            start_address = int(operand, 16)
            locctr = start_address
            if label:
                symtab.add_symbol(label, locctr)
            # Move to the next line
            source_lines = source_lines[1:]
        else:
            # No START directive, address defaults to 0
            start_address = 0
            locctr = 0

        # Main processing loop
        for line in source_lines:
            # Ignore comments
            if line.strip().startswith('.'):
                continue

            label, mnemonic, operand = self.parser.parse(line)

            # If there's a label, add it to SYMTAB
            if label:
                symtab.add_symbol(label, locctr)

            # Increment LOCCTR based on mnemonic
            if self.optab.is_mnemonic(mnemonic):
                locctr += 3
            elif mnemonic == 'WORD':
                locctr += 3
            elif mnemonic == 'RESW':
                locctr += 3 * int(operand)
            elif mnemonic == 'RESB':
                locctr += int(operand)
            elif mnemonic == 'BYTE':
                # For C'EOF' -> 3 bytes, for X'F1' -> 1 byte
                if operand.upper().startswith('C'):
                    locctr += len(operand) - 3 # Length of string inside C''
                elif operand.upper().startswith('X'):
                    locctr += (len(operand) - 3) // 2 # Length of hex string / 2
            elif mnemonic == 'END':
                break
            else:
                raise ValueError(f"Invalid operation code: {mnemonic}")

        program_length = locctr - start_address
        return symtab, program_length

