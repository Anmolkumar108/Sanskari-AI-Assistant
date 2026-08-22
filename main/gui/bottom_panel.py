from PyQt6.QtWidgets import (
    QLabel,
    QTextEdit,
    QHBoxLayout,
)

from main.gui.components.hud_panel import HudPanel
from main.core.event_bus import event_bus


class BottomPanel(HudPanel):

    def __init__(self):
        super().__init__()

        self.setFixedHeight(170)

        # -------------------------
        # Status Label
        # -------------------------

        self.status = QLabel("STATUS : READY")

        self.status.setStyleSheet("""
            color:#00FF99;
            font-size:18px;
            background:transparent;
            padding:4px;
        """)

        self.layout.addWidget(self.status)

        # ==========================
        # Split Layout
        # ==========================
        split_layout = QHBoxLayout()

        # Chat Box
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setStyleSheet("""
            QTextEdit{
                background:#05080F;
                color:white;
                border:1px solid #00E5FF;
                font-size:15px;
                padding:6px;
            }
        """)

        # Log Box (existing)
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        self.logs.setStyleSheet("""
            QTextEdit{
                background:#05080F;
                color:#00E5FF;
                border:1px solid #00E5FF;
                font-size:15px;
                padding:6px;
            }
        """)

        self.logs.append("System Ready...")

        split_layout.addWidget(self.chat, 3)
        split_layout.addWidget(self.logs, 2)

        self.layout.addLayout(split_layout)

        # Event Bus Listening
        event_bus.state_changed.connect(self.update_status)
        event_bus.log_message.connect(self.add_log)
        event_bus.user_message.connect(self.add_user_message)
        event_bus.assistant_message.connect(self.add_ai_message)

    def update_status(self, state):

        self.status.setText(f"STATUS : {state}")

        self.logs.append(f">>> {state}")

    def add_log(self, message):

        self.logs.append(f"> {message}")

        scrollbar = self.logs.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def add_user_message(self, text):

        self.chat.append(
            f"<span style='color:#00E5FF;'><b>👤 YOU</b></span><br>"
            f"<span style='color:white;'>{text}</span><br><br>"
        )

        scrollbar = self.chat.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def add_ai_message(self, text):

        print("AI MESSAGE RECEIVED =", text)

        self.chat.append(
            f"<span style='color:#00FF99;'><b>🤖 SANSKARI AI</b></span><br>"
            f"<span style='color:white;'>{text}</span><br><br>"
        )

        scrollbar = self.chat.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())