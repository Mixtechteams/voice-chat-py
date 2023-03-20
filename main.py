from datetime import datetime
import os
from modules.com_button_listener import ComButtonListener
from modules.print_log import print_log
import argparse;
from twisted.internet import reactor, tksupport, task
from modules.ui import UI
from queue import Queue

from modules.voice_chat import VoiceChat

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'Переговорное устройство')
    parser.add_argument('--port', type=int)
    parser.add_argument('--address')
    parser.add_argument('--comport')
    args = parser.parse_args()
    
    port = args.port
    address = args.address
    com_port = args.comport
    is_host = len(com_port or '') == 0
    print(address, port)
    
    voice_chat = VoiceChat(address, port, use_recognizer=is_host)

    if is_host:
        ui = UI(on_mic_state_changed=lambda enabled: voice_chat.set_mic_enabled(enabled), on_print_click=lambda: print_log(ui.get_log()))
        
        message_queue = Queue()
        def add_new_message(ip, text):
            now = datetime.now()
            message_queue.put((ip, now.strftime("%H:%M:%S"), text))

        def on_closing():
            ui.window.quit()
            reactor.stop()
            os._exit(0)

        ui.window.protocol("WM_DELETE_WINDOW", lambda: reactor.callFromThread(on_closing))
        tksupport.install(ui.window)

        voice_chat.on_message_received = add_new_message
        tksupport.install(ui.window)

        def queue_h():
            try:
                item = message_queue.get(False)

                ui.add_message(*item)
            except:
                pass
        task.LoopingCall(queue_h).start(0.1)
    else:
        button_listener = ComButtonListener(com_port, lambda enabled: voice_chat.set_mic_enabled(enabled))
        task.LoopingCall(button_listener.update).start(0.1)

    reactor.listenMulticast(args.port, voice_chat, listenMultiple=True)
    reactor.run()
