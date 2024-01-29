import logging

class ADF4351:
    def update(self):
        """ Update all PLL registers. """
        for value in reversed(self._regs):
            # write registers in order R5..R0, according to datasheet.
            self.write(value)

    def set_fields(self, *fields):
        """ Set PLL register fields. """
        for field in fields:
            self._regs[field.REG] &= field.zeros_mask()
            self._regs[field.REG] |= field._value << field.OFFSET

    def __init__(self, device, fref, fpfd):
        self._log = logging.getLogger(__name__)
        self._dev = device
        self._fref = fref
        self._fpfd = fpfd

        self._regs = [
            0x05b90348, # R0
            0x0800fff9, # R1
            0x180b1e42, # R2
            0x00200003, # R3
            0x00801434, # R4
            0x00400005, # R5
        ]

        self.set_vco_freq(3e9)
        self.update()

    def write(self, value):
        """ Write PLL register. """
        bytesval = value.to_bytes(4)
        self._log.debug(f"> 0x{value:08x}")
        self._dev.writebytes(bytesval)

    def set_vco_freq(self, fvco):
        """ Set PLL VCO frequency, calculating all register parameters. """
        if not 2.2e9 <= fvco <= 4.4e9:
            raise ValueError(fvco)

        mod = 4095
        rdiv = self._fref / self._fpfd
        realdiv = fvco / self._fpfd
        n = int(realdiv)
        frac = round(mod * (realdiv - n))
        realfvco = self._fpfd * (n + frac / mod)

        dint = DivInteger(n)
        dfrac = DivFractional(frac)

        self._log.info(f"n={n} frac={frac}, realfvco={realfvco}")

        self.set_fields(dint, dfrac)
