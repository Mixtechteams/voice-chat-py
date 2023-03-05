import socket

class UdpMessageSender():
    def __init__(self, address: str, port: int) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect((address, port))

    def send(self, data: str):
        self.socket.send(data.encode())
