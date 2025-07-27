class Registers:
    """
    Represents the register set for the SIC machine.
    All registers (A, X, L, PC, SW) are 24 bits wide.
    """
    
    # Use __slots__ to prevent the creation of arbitrary attributes on the instance.
    # This ensures that only the defined SIC registers can be accessed, making
    # test_invalid_register_access pass.
    __slots__ = ['_A', '_X', '_L', '_PC', '_SW']

    def __init__(self):
        """
        Initializes all registers to 0.
        """
        self._A = 0
        self._X = 0
        self._L = 0
        self._PC = 0
        self._SW = 0

    @property
    def A(self):
        return self._A

    @A.setter
    def A(self, value):
        self._A = value & 0xFFFFFF

    @property
    def X(self):
        return self._X

    @X.setter
    def X(self, value):
        self._X = value & 0xFFFFFF

    @property
    def L(self):
        return self._L

    @L.setter
    def L(self, value):
        self._L = value & 0xFFFFFF

    @property
    def PC(self):
        return self._PC

    @PC.setter
    def PC(self, value):
        self._PC = value & 0xFFFFFF

    @property
    def SW(self):
        return self._SW

    @SW.setter
    def SW(self, value):
        self._SW = value & 0xFFFFFF

