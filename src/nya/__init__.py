import logging
import json
import click
from serial import Serial
import time

from . import tt7000
from .tt7000 import TT7000


logger = logging.getLogger(__name__)


@click.command()
@click.option('--siggen')
@click.option('-o', '--output', type=click.File(mode='w'), default='-')
@click.option('-f', '--from', 'from_', type=int, default=300)
@click.option('-t', '--to', type=int, default=500)
@click.option('-s', '--step', type=int, default=1)
def cli(siggen, output, from_, to, step):
    logging.basicConfig(level=logging.DEBUG)

    hw = TT7000(Serial(siggen, 115200))
    try:
        hw.set_mode(tt7000.Mode.SIG_GEN_AND_METER)
        hw.enable_buzzer(False)
        hw.enable_output()

        for freq in range(from_, to, step):
            freq = int(freq*1e6) # MHz -> Hz

            hw.set_gen_freq(freq)
            pwr = hw.read_power()
            output.write(json.dumps({'F': freq, 'P': pwr}) + '\n')

    finally:
        hw.close()
