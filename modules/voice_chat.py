import asyncio
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
model: Model | None = None

class VoiceChat(DatagramProtocol):
    on_message_received: Callable[[str, str], None]
    mic_enabled: bool = False

    def __init__(self, ip: str, port: int, use_recognizer: bool):
        if use_recognizer:
            global model; model = model or Model("model")
        self.ip = ip
        self.port = port
        self.use_recognizer = use_recognizer
        self.my_ips = [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None)]

    def set_mic_enabled(self, mic_enabled: bool):
        self.mic_enabled = mic_enabled

    def startProtocol(self):
        py_audio = pyaudio.PyAudio()
        self.buffer = BUFFER  
        
        self.another_client = self.ip, self.port
        
        if self.use_recognizer:
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
            
            if self.use_recognizer:
                text = self.recognize_text(self.outrec, data)
                if text != None:
                    self.on_message_received(self.my_ips[-1], text)

    # прием голоса, преобразование в текст и логирование, воспроизведение если передача не с этого клиента
    def datagramReceived(self, datagram, addr):
        if addr[0] in self.my_ips:
            return
        
        self.output_stream.write(datagram)
        text = self.recognize_text(self.rec, datagram)
        if text != None:
            self.on_message_received(addr, text)
            
    def recognize_text(self, recognizer, data):
        if self.use_recognizer and recognizer.AcceptWaveform(data):
            res = recognizer.Result()
            message: str = json.loads(res)['text']
    
            if len(message) > 0 and self.on_message_received:
                return message
        return None
