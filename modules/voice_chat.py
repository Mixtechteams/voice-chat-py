import socket
from typing import Callable
from vosk import Model, KaldiRecognizer
import json
import pyaudio
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

FRAME_RATE = 44100
BUFFER = 4096
CHANNELS=1
model = Model("model")

class VoiceChat(DatagramProtocol):
    on_message_received: Callable[[str, str], None]
    mic_enabled: bool = False

    def __init__(self, ip: str, port: int):
        hostname=socket.gethostname()   
        IPAddr=socket.gethostbyname(hostname)   
        self.ip = ip
        self.port = port
        self.my_ip = IPAddr

    def set_mic_enabled(self, mic_enabled: bool):
        self.mic_enabled = mic_enabled

    def startProtocol(self):
        py_audio = pyaudio.PyAudio()
        self.buffer = BUFFER  
        
        self.another_client = self.ip, self.port
        
        self.rec = KaldiRecognizer(model, FRAME_RATE)
        self.rec.SetWords(True)
        self.outrec = KaldiRecognizer(model, FRAME_RATE)
        self.outrec.SetWords(True)
        
        # группа для мультикаст передачи, так же остается передача напрямую по ip
        self.transport.joinGroup(self.ip)

        # выдаст ошибку если нет колонок
        self.output_stream = py_audio.open(format=pyaudio.paInt16,
                                           output=True, rate=FRAME_RATE, channels=CHANNELS,
                                           frames_per_buffer=self.buffer)
        
        # выдаст ошибку если нет микрофона
        self.input_stream = py_audio.open(format=pyaudio.paInt16,
                                          input=True, rate=FRAME_RATE, channels=CHANNELS,
                                          frames_per_buffer=self.buffer)
        reactor.callInThread(self.record)

    # передача голоса по ип либо всем мультикаст
    def record(self):
        while True:
            if not self.mic_enabled:
                continue

            data = self.input_stream.read(self.buffer,exception_on_overflow=False)
            self.transport.write(data, self.another_client)
            
            self.outrec.AcceptWaveform(data)

    # прием голоса, преобразование в текст и логирование, воспроизведение если передача не с этого клиента
    def datagramReceived(self, datagram, addr):
        if addr[0]!=self.my_ip:
            self.output_stream.write(datagram)
            
        if self.rec.AcceptWaveform(datagram):
            res = self.rec.Result()
            message: str = json.loads(res)['text']

            if len(message) > 0 and self.on_message_received:
                self.on_message_received(addr, message)

def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

