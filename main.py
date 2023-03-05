from modules.udp_message_sender import UdpMessageSender;
import argparse;
from twisted.internet import reactor

from modules.voice_chat import VoiceChat

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'Переговорное устройство')
    parser.add_argument('--port', type=int)
    parser.add_argument('--address')
    args = parser.parse_args()
    
    port = args.port
    address = args.address
    print(address, port)

    voiceChat = VoiceChat(address, port)
    voiceChat.on_message_received = lambda ip, text: print(ip, text)
    reactor.listenMulticast(args.port, voiceChat, listenMultiple=True)
    reactor.run()
    # message_sender = UdpMessageSender(address, port)