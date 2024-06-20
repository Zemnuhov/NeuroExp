from pathlib import Path
from numpy import uint8
from ctypes import windll
import platform

from neuroexplib.trigger.trigger import Trigger


class ParallelPort(Trigger):
    def __init__(self, port=0x0378):
        if isinstance(port, str) and port.startswith("0x"):
            self.base = int(port, 16)
        else:
            self.base = port

        if platform.architecture()[0] == "32bit":
            self.port = getattr(windll, str(Path.cwd() / "inpout32.dll"))
        elif platform.architecture()[0] == "64bit":
            print(Path.cwd())
            self.port = getattr(windll, str(Path.cwd() / "inpoutx64.dll"))
        BYTEMODEMASK = uint8(1 << 5 | 1 << 6 | 1 << 7)
        _inp = self.port.Inp32(self.base + 0x402)
        self.port.Out32(self.base + 0x402, int((_inp & ~BYTEMODEMASK) | (1 << 5)))
        _inp = self.port.Inp32(self.base + 2)
        self.port.Out32(self.base + 2, int(_inp & ~uint8(1 << 5)))
        self.status = None

    def set_data(self, data):
        self.port.Out32(self.base, data)

    def set_pin(self, pinNumber, state):
        _inp = self.port.Inp32(self.base)
        if state:
            val = _inp | 2 ** (pinNumber - 2)
        else:
            val = _inp & (255 ^ 2 ** (pinNumber - 2))
        self.port.Out32(self.base, val)

    def read_data(self):
        return self.port.Inp32(self.base)

    def read_pin(self, pinNumber):
        _base = self.port.Inp32(self.base + 1)
        if pinNumber == 10:
            # 10 = ACK
            return (_base >> 6) & 1
        elif pinNumber == 11:
            # 11 = BUSY
            return (_base >> 7) & 1
        elif pinNumber == 12:
            # 12 = PAPER-OUT
            return (_base >> 5) & 1
        elif pinNumber == 13:
            # 13 = SELECT
            return (_base >> 4) & 1
        elif pinNumber == 15:
            # 15 = ERROR
            return (_base >> 3) & 1
        elif 2 <= pinNumber <= 9:
            return (self.port.Inp32(self.base) >> (pinNumber - 2)) & 1
        else:
            msg = "Pin %i cannot be read (by PParallelInpOut32.readPin())"
            print(msg % pinNumber)
