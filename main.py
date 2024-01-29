import spidev
import logging
from argparse import ArgumentParser

if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('--pfd', type=int, default=1000000, help="PFD frequency [Hz]")
    p.add_argument('--ref', type=int, default=44000000, help="REF input frequency [Hz]")
    p.add_argument('--referr', type=float, default=0, help="REF oscillator error [ppm]")
    p.add_argument('--div', type=int, choices=[1, 2, 4, 8, 16, 32, 64], default=1, help="Output divider factor []")
    p.add_argument('--loglevel', choices=['debug', 'info', 'warning', 'error', 'critical'], default='debug')
    p.add_argument('--bus', type=int, default=0, help="PLL SPI bus number")
    p.add_argument('--device', type=int, default=0, help="PLL SPI device number")
    p.add_argument('output', type=float, help="VCO output frequency [Hz]")
    args = p.parse_args()

    logging.basicConfig(level=args.loglevel.upper())

    dev = spidev.SpiDev()
    dev.open(args.bus, args.device)

    pll = ADF4351(dev, fref=args.ref, fpfd=args.pfd)
    pll.set_vco_freq(args.output * (1 + args.referr * 1e-6))
    pll.set_fields(
        OutputDivider(OutputDividerFactor(args.div))
    )
    pll.update()
