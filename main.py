from datetime import datetime
import os
from modules.print_log import print_log
from modules.udp_message_sender import UdpMessageSender;
import argparse;
from twisted.internet import reactor, tksupport
from modules.ui import UI

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

    ui = UI(on_mic_state_changed=lambda enabled: voiceChat.set_mic_enabled(enabled), on_print_click=lambda: print_log(ui.get_log()))
    
    def add_new_message(ip, text):
        now = datetime.now()
        ui.add_message(ip, now.strftime("%H:%M:%S"), text)

    def on_closing():
        ui.window.quit()
        reactor.stop()
        os._exit(0)

    ui.window.protocol("WM_DELETE_WINDOW", lambda: reactor.callFromThread(on_closing))
    tksupport.install(ui.window)

    voiceChat.on_message_received = add_new_message
    reactor.listenMulticast(args.port, voiceChat, listenMultiple=True)
    tksupport.install(ui.window)
    reactor.run()
    # message_sender = UdpMessageSender(address, port)