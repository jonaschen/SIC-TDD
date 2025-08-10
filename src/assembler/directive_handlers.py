from abc import ABC, abstractmethod

class DirectiveHandler(ABC):
    """
    Abstract base class for a directive handling strategy.
    """
    @abstractmethod
    def handle(self, operand: str | None) -> int:
        """
        Calculates the number of bytes this directive reserves.

        Args:
            operand: The operand from the source line.

        Returns:
            The number of bytes to add to the location counter.
        """
        pass

class WordDirectiveHandler(DirectiveHandler):
    """Handles the WORD directive."""
    def handle(self, operand: str | None) -> int:
        return 3

class ReswDirectiveHandler(DirectiveHandler):
    """Handles the RESW directive."""
    def handle(self, operand: str | None) -> int:
        if operand is None:
            raise ValueError("RESW requires an operand.")
        return 3 * int(operand)

class ResbDirectiveHandler(DirectiveHandler):
    """Handles the RESB directive."""
    def handle(self, operand: str | None) -> int:
        if operand is None:
            raise ValueError("RESB requires an operand.")
        return int(operand)

class ByteDirectiveHandler(DirectiveHandler):
    """Handles the BYTE directive."""
    def handle(self, operand: str | None) -> int:
        if operand is None:
            raise ValueError("BYTE requires an operand.")
        
        operand_upper = operand.upper()
        if operand_upper.startswith('C'):
            # Length of string inside C'...'
            return len(operand) - 3
        elif operand_upper.startswith('X'):
            # Length of hex string / 2
            return (len(operand) - 3) // 2
        else:
            raise ValueError(f"Invalid BYTE operand format: {operand}")

