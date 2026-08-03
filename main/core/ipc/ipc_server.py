import socket
import threading
import traceback

from main.core.event_bus import event_bus
from main.core.ipc.messages import parse_message


HOST = "127.0.0.1"
PORT = 8765


class IPCServer:

    def __init__(self):

        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.server.bind((HOST, PORT))

        self.server.listen(1)

    def start(self):

        threading.Thread(
            target=self.accept,
            daemon=True
        ).start()

    def accept(self):

        while True:

            conn, addr = self.server.accept()
            print("CLIENT CONNECTED:", addr)

            threading.Thread(
                target=self.handle,
                args=(conn,),
                daemon=True
            ).start()

    