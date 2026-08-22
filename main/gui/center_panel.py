from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from main.animations.jarvis_ring import JarvisRing
from main.core.event_bus import event_bus


class CenterPanel(QWidget):

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.setStyleSheet("""
            QWidget{
                background:#05080F;
                border:2px solid #00E5FF;
                border-radius:15px;
            }

            QLabel{
                color:white;
                background:transparent;
            }
        """)

        layout = QVBoxLayout()

        layout.addStretch()

        self.title = QLabel("SANSKARI AI")

        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title.setStyleSheet("""
            font-size:32px;
            color:#00E5FF;
            font-weight:bold;
        """)

        layout.addWidget(self.title)

        layout.addSpacing(25)

        # Animated Ring
        self.ai_core = JarvisRing()
        layout.addWidget(
            self.ai_core,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addSpacing(25)

        self.status = QLabel("STATUS : IDLE")

        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status.setStyleSheet("""
            font-size:18px;
            color:#00FF99;
        """)

        layout.addWidget(self.status)

        # Step 25: Live Message Label
        self.message = QLabel("Ready")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message.setStyleSheet("""
            font-size:16px;
            color:#AAAAAA;
        """)

        layout.addWidget(self.message)

        layout.addStretch()

        self.setLayout(layout)

        # Event Bus Listening
        event_bus.state_changed.connect(self.update_state)
        event_bus.message_received.connect(self.update_message)

    def update_state(self, state):

        self.status.setText(f"STATUS : {state}")

        self.ai_core.set_state(state)

    def update_message(self, message):

        self.message.setText(message)