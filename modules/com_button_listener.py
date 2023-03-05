import binascii

from typing import Callable
from serial import Serial, SerialException

class ComButtonListener:
    def __init__(self, port_name, on_button_state_change: Callable[[bool], None] | None = None) -> None:
        print()
        self.on_button_state_change = on_button_state_change
        self.serial = Serial(baudrate=9600, timeout=1000, write_timeout=1000)
        for i in range(5):
            self.serial.port = port_name

            try:
                self.serial.open()
            except SerialException as e:
                print(f'Error while opening. Attempt {i+1}/5. Base error: {e}')
            else:
                break

        if not self.serial.is_open:
            raise (RuntimeError('Error: could not open port'))

    def update(self):
        total_read = 0
        attempts = 10

        while total_read % 3 != 0:
            r = self.serial.read(3)
            r = binascii.hexlify(bytearray(r))
            arr = r[total_read % 3:3 - total_read % 3]

            total_read += len(arr)
            
            attempts = attempts - 1
            if attempts <= 0:
                break

        if self.on_button_state_change:
            self.on_button_state_change(arr[1] & 0b10000000 > 0)
