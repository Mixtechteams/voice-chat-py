from typing import Callable
import serial

class ComButtonListener:
    def __init__(self, port_name, on_button_state_change: Callable[[bool], None] | None = None) -> None:
        self.on_button_state_change = on_button_state_change
        self.serial = serial.Serial(baudrate=9600, timeout=1000, write_timeout=1000)
        for i in range(5):
            self.serial.port = port_name

            try:
                self.serial.open()
            except serial.SerialException as e:
                print(f'Error while opening. Attempt {i+1}/5. Base error: {e}')
            else:
                break

        if not self.serial.is_open:
            raise (RuntimeError('Error: could not open port'))
            
        message = bytearray([0xa1, 0, 0x86])  # 100

        # Команда старта
        self.serial.write(message)



    def update(self):
        buffer = bytearray(3)
        
        if self.serial.inWaiting() < 3:
            return

        buffer = self.serial.read(self.serial.inWaiting())
        index = buffer.rfind(0xb1)
        if index + 1 >= len(buffer):
            index = index - 2
        else:
            index = index + 1

        if self.on_button_state_change:
            self.on_button_state_change(buffer[index] & 0b10000000 > 0)
