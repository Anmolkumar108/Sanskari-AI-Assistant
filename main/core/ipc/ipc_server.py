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

    def handle(self, conn):

        buffer = ""

        while True:

            try:

                data = conn.recv(4096)

                if not data:
                    break

                buffer += data.decode()

                while "\n" in buffer:

                    raw_msg, buffer = buffer.split("\n", 1)

                    if not raw_msg.strip():
                        continue

                    # print("📨 RAW:", raw_msg)

                    msg = parse_message(raw_msg)
                    # print("📨 PARSED:", msg)
                    # print("MESSAGE:", msg)

                    event = msg["event"]
                    value = msg["data"]

                    # print("EVENT =", event)
                    # print("VALUE =", value)

                    if event == "state":
                        event_bus.state_changed.emit(value)

                    elif event == "log":
                        event_bus.log_message.emit(value)

                    elif event == "chat":
                        event_bus.chat_message.emit(value)

                    elif event == "user_message":
                        event_bus.user_message.emit(value)

                    elif event == "assistant_message":
                        event_bus.assistant_message.emit(value)
                        event_bus.message_received.emit(value)

                    elif event == "tool":
                        event_bus.tool_changed.emit(value)

                    elif event == "command":
                        event_bus.last_command_changed.emit(value)

                    elif event == "response":
                        event_bus.response_changed.emit(value)
                        event_bus.message_received.emit(value)

                    