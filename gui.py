import subprocess
import sys
import os

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt


class AIGirlUI(QWidget):

    def __init__(self):
        super().__init__()

        # =================================
        # WINDOW
        # =================================

        self.setWindowTitle("💖 Sanskari AI")
        self.setFixedSize(1000, 600)

        self.process = None

        # =================================
        # CURRENT PATH
        # =================================

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # GIF PATHS
        self.idle_gif = os.path.join(
            BASE_DIR,
            "main",
            "assets",
            "idle.gif"
        )

        self.talking_gif = os.path.join(
            BASE_DIR,
            "main",
            "assets",
            "talking.gif"
        )

        # AGENT PATH
        self.agent_file = os.path.join(
            BASE_DIR,
            "main",
            "agent.py"
        )

        # =================================
        # STYLE
        # =================================

        self.setStyleSheet("""

            QWidget{
                background-color: #0f0f0f;
                color: white;
                font-size: 18px;
                font-family: Arial;
            }

            QPushButton{
                background-color: #ff4da6;
                border-radius: 20px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
            }

            QPushButton:hover{
                background-color: #ff1a8c;
            }

        """)

        # =================================
        # MAIN LAYOUT
        # =================================

        main_layout = QHBoxLayout()

        # =================================
        # LEFT SIDE
        # =================================

        left_layout = QVBoxLayout()

        self.avatar = QLabel()

        self.avatar.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # =================================
        # IDLE GIF
        # =================================

        self.movie = QMovie(self.idle_gif)

        # DEBUG
        if self.movie.isValid():
            print("✅ Idle GIF Loaded")
        else:
            print("❌ Idle GIF NOT Found")

        self.avatar.setMovie(self.movie)

        self.movie.start()

        left_layout.addWidget(self.avatar)

        # =================================
        # RIGHT SIDE
        # =================================

        right_layout = QVBoxLayout()

        self.title = QLabel(
            "💖 Sanskari AI Assistant"
        )

        self.title.setStyleSheet("""

            font-size: 30px;
            font-weight: bold;
            color: #ff4da6;

        """)

        self.status = QLabel(
            "Status : Waiting..."
        )

        self.status.setStyleSheet("""

            font-size: 20px;
            color: #00ff99;

        """)

        self.chat = QLabel(
            "Hello Anmol ❤️\nMain Sanskari hoon..."
        )

        self.chat.setWordWrap(True)

        self.chat.setStyleSheet("""

            background-color: #1e1e1e;
            border-radius: 20px;
            padding: 20px;
            font-size: 20px;

        """)

        # =================================
        # BUTTONS
        # =================================

        self.start_btn = QPushButton(
            "🎤 Start Sanskari"
        )

        self.stop_btn = QPushButton(
            "🛑 Stop Sanskari"
        )

        self.start_btn.clicked.connect(
            self.start_ai
        )

        self.stop_btn.clicked.connect(
            self.stop_ai
        )

        # =================================
        # ADD WIDGETS
        # =================================

        right_layout.addWidget(self.title)

        right_layout.addSpacing(20)

        right_layout.addWidget(self.status)

        right_layout.addSpacing(20)

        right_layout.addWidget(self.chat)

        right_layout.addStretch()

        right_layout.addWidget(self.start_btn)

        right_layout.addWidget(self.stop_btn)

        # =================================
        # FINAL LAYOUT
        # =================================

        main_layout.addLayout(left_layout, 1)

        main_layout.addLayout(right_layout, 1)

        self.setLayout(main_layout)

    # =================================
    # START AI
    # =================================

    def start_ai(self):

        self.status.setText(
            "Status : Sanskari Speaking..."
        )

        self.chat.setText(
            "Hello Anmol ❤️\nMain aa gayi..."
        )

        # =================================
        # CHANGE TO TALKING GIF
        # =================================

        self.movie.stop()

        self.movie = QMovie(self.talking_gif)

        if self.movie.isValid():
            print("✅ Talking GIF Loaded")
        else:
            print("❌ Talking GIF NOT Found")

        self.avatar.setMovie(self.movie)

        self.movie.start()

        # =================================
        # RUN AGENT
        # =================================

        try:

            if self.process is None:

                self.process = subprocess.Popen(
                    [sys.executable, self.agent_file, "console"],
                    cwd=os.path.dirname(self.agent_file)
                )

                self.chat.setText(
                    "💖 Sanskari Started Successfully"
                )

        except Exception as e:

            self.chat.setText(
                f"Error : {str(e)}"
            )

    # =================================
    # STOP AI
    # =================================

    def stop_ai(self):

        self.status.setText(
            "Status : Stopped"
        )

        self.chat.setText(
            "Bye Anmol ❤️"
        )

        try:

            if self.process:

                self.process.kill()

                self.process = None

        except:
            pass

        # =================================
        # BACK TO IDLE
        # =================================

        self.movie.stop()

        self.movie = QMovie(self.idle_gif)

        self.avatar.setMovie(self.movie)

        self.movie.start()

    # =================================
    # CLOSE WINDOW
    # =================================

    def closeEvent(self, event):

        try:

            if self.process:
                self.process.kill()

        except:
            pass

        event.accept()


# =================================
# MAIN APP
# =================================

app = QApplication(sys.argv)

window = AIGirlUI()

window.show()

sys.exit(app.exec())
