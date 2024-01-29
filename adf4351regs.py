from enum import Enum

# base register field classes
class RegisterField:
    REG_LEN = 32

    @classmethod
    def ones_mask(cls):
        return (2 ** cls.LEN - 1) << cls.OFFSET

    @classmethod
    def zeros_mask(cls):
        return 2**32 - cls.ones_mask() - 1

class BitRegisterField(RegisterField):
    LEN = 1

    def __init__(self, value):
        self._value = bool(value)

# field definitions
class DivFractional(RegisterField):
    # RF divider fractional part
    REG = 0
    OFFSET = 3
    LEN = 12

    def __init__(self, value):
        # validate value
        self._value = value

class DivInteger(RegisterField):
    # RF divider integer part
    REG = 0
    OFFSET = 15
    LEN = 16

    def __init__(self, value):
        if not 75 <= value <= 65535:
            raise ValueError(value)
        self._value = value

class DivModulus(RegisterField):
    # RF divider fractional modulus
    REG = 1
    OFFSET = 3
    LEN = 12

    def __init__(self, value):
        if not 2 <= value <= 4095:
            raise ValueError(value)
        self._value = value

class OutputDividerFactor(Enum):
    DIV1 = 0
    DIV2 = 1
    DIV4 = 2
    DIV8 = 3
    DIV16 = 4
    DIV32 = 5
    DIV64 = 6

class OutputDivider(RegisterField):
    # output divider value
    REG = 4
    OFFSET = 20
    LEN = 3

    def __init__(self, factor):
        self._value = factor.value

class PowerDown(BitRegisterField):
    # Chipset power down
    REG = 2
    OFFSET = 5

class RFOutAEnabled(BitRegisterField):
    # RF output A output stage enabled
    REG = 4
    OFFSET = 5

class RFOutAPower(RegisterField):
    # RF Output A output power
    REG = 4
    OFFSET = 3
