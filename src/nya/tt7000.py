import logging
from enum import Enum
from serial import Serial
import re

READ_POWER_RE = re.compile(r'([-+]?\d+.\d+)dBm')

logger = logging.getLogger(__name__)

class Mode(Enum):
    METER_COUNTER = 'METERCOUNTER'
    SIG_GEN_AND_METER = 'SIGGENMETER'
    SIG_GEN = 'SIGNALGEN'

class TT7000Error(Exception): ...

class TT7000:
    def __init__(self, port: Serial):
        self.serial = port

    def _expect_ok(self):
        resp = self.serial.readline()
        logger.debug(f'[>] {resp}')
        if not resp.startswith(b'OK'):
            raise TT7000Error(f'expected OK, got `{resp}`!')

    def set_mode(self, mode: Mode):
        self.serial.write(f'SYST:MODE {mode.value}\n'.encode('ascii'))
        self._expect_ok()

    def set_output_on(self, on: bool = True):
        on = 'ON' if on else 'OFF'
        self.serial.write(f'OUTP:STAT {on}\n'.encode('ascii'))

    def set_gen_freq(self, freq: float):
        self.serial.write(f'FREQ:CW {int(freq)}Hz\n'.encode('ascii'))

    def read_power(self) -> float: # dBm
        self.serial.write(b'POWER:READ?\n')
        resp = self.serial.readline()
        logger.debug(f'[>] read power: {resp}')
        if m := READ_POWER_RE.match(resp.decode('ascii')):
            return m[1]
        else:
            raise TT7000Error(f'did a `POWER:READ?` but got an unparsable response: `{resp}`')

    def close(self):
        self.serial.close()
