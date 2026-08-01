import socket
import time

from main.core.ipc.messages import create_message

HOST = "127.0.0.1"
PORT = 8765


class IPCClient:

    def __init__(self):

        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        connected = False

        while not connected:

            try:
                self.client.connect((HOST, PORT))
                connected = True

            except ConnectionRefusedError:
                time.sleep(0.5)

    