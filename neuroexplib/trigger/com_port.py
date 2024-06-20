
from neuroexplib.trigger.trigger import Trigger


class COMPort(Trigger):
    def __init__(self, port='COM1', baudrate=9600, timeout=1):
        import serial

        self.port_name = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_port = serial.Serial(
            port=self.port_name,
            baudrate=self.baudrate,
            timeout=self.timeout
        )

    def set_data(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.serial_port.write(data)

    def read_data(self, size=1):
        return self.serial_port.read(size)

    def set_baudrate(self, baudrate):
        self.serial_port.baudrate = baudrate

    def get_baudrate(self):
        return self.serial_port.baudrate

    def close(self):
        self.serial_port.close()
