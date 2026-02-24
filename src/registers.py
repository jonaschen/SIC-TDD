class Registers:
    """
    Represents the register set for the SIC machine.
    All registers (A, X, L, PC, SW) are 24 bits wide.
    Additional SIC/XE registers (B, S, T) are 24 bits wide, and F is 48 bits wide.
    """
    
    # Mode constants
    SUPERVISOR = 0
    USER = 1

    # Use __slots__ to prevent the creation of arbitrary attributes on the instance.
    # This ensures that only the defined SIC registers can be accessed, making
    # test_invalid_register_access pass.
    __slots__ = ['_A', '_X', '_L', '_PC', '_SW', '_B', '_S', '_T', '_F']

    def __init__(self):
        """
        Initializes all registers to 0.
        """
        self._A = 0
        self._X = 0
        self._L = 0
        self._PC = 0
        self._SW = 0
        self._B = 0
        self._S = 0
        self._T = 0
        self._F = 0

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

    @property
    def mode(self):
        """
        Returns the current mode of the machine based on SW bit 6.
        0 = Supervisor, 1 = User.
        """
        return (self._SW >> 6) & 1

    @mode.setter
    def mode(self, value):
        """
        Sets the mode of the machine by updating SW bit 6.
        """
        if value == self.USER:
            self._SW |= 0x40
        else:
            self._SW &= 0xFFFFBF

    @property
    def B(self):
        return self._B

    @B.setter
    def B(self, value):
        self._B = value & 0xFFFFFF

    @property
    def S(self):
        return self._S

    @S.setter
    def S(self, value):
        self._S = value & 0xFFFFFF

    @property
    def T(self):
        return self._T

    @T.setter
    def T(self, value):
        self._T = value & 0xFFFFFF

    @property
    def F(self):
        return self._F

    @F.setter
    def F(self, value):
        self._F = value & 0xFFFFFFFFFFFF
