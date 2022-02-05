import logging
import click
from serial import Serial
import time

from . import tt7000
from .tt7000 import TT7000


logger = logging.getLogger(__name__)


@click.command()
@click.option('--siggen')
def cli(siggen):
    logging.basicConfig(level=logging.DEBUG)

    hw = TT7000(Serial(siggen, 115200))
    try:
        hw.set_mode(tt7000.Mode.SIG_GEN_AND_METER)
        time.sleep(0.1)
        hw.set_output_on()
        time.sleep(0.1)
        for freq_mhz in range(300, 400):
            hw.set_gen_freq(freq_mhz*1e6)
            # time.sleep(0.1)
            print(freq_mhz, hw.read_power())
            # time.sleep(0.1)


    finally:
        hw.close()
