from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QTimer
from datetime import datetime


class ClockWidget(QLabel):

    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("""
            QLabel{
                color:#00E5FF;
                font-size:18px;
                font-weight:bold;
                background:transparent;
            }
        """)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.update_time()

    def update_time(self):
        current = datetime.now().strftime("%d-%m-%Y   %I:%M:%S %p")
        self.setText(current)