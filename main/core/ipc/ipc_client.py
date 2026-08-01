import socket
import time

from main.core.ipc.messages import create_message

HOST = "127.0.0.1"
PORT = 8765


class IPCClient:

    def __init__(self):

        