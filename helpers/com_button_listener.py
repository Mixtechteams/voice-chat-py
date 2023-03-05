import binascii

import serial
from sys import argv
from typing import Callable

def listen_port(port_name, on_button_pressed: Callable | None = None, on_button_release: Callable | None =None):
    with serial.Serial(baudrate=9600, timeout=1000, write_timeout=1000) as ser:
        for i in range(5):
            ser.port = port_name

            try:
                ser.open()
            except serial.SerialException as e:
                print(f'Error while opening. Attempt {i+1}/5. Base error: {e}')
            else:
                break

        if not ser.is_open:
            print('Error: could not open port')
            exit(-1)

        cmd = bytearray([0xA1, 0x00, 0x86])
        ser.write(cmd)

        total_read = 0

        while True:
            r = ser.read(3)
            r = binascii.hexlify(bytearray(r))
            arr = r[total_read % 3:3 - total_read % 3]

            total_read += len(arr)

            if total_read % 3 != 0:
                continue

            if arr[1] & 0b10000000 > 0:
                if on_button_pressed:
                    on_button_pressed()
            else:
                if on_button_release:
                    on_button_release()