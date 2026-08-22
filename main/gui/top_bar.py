from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, QTimer, QTime


class TopBar(QWidget):

    def __init__(self):
        super().__init__()

        self.setFixedHeight(60)

        self.setStyleSheet("""
            background:#08111F;
            border:1px solid #00E5FF;
            border-radius:8px;
        """)

        layout = QHBoxLayout()

        self.title = QLabel("🤖 Sanskari AI")
        self.status = QLabel("🟢 ONLINE")
        self.clock = QLabel()
        self.close_btn = QPushButton("✕")

        # Title Styling
        self.title.setStyleSheet("""
            color:#00E5FF;
            font-size:22px;
            font-weight:bold;
            border:none;
        """)

        # Status Styling
        self.status.setStyleSheet("""
            color:#00FF99;
            font-size:14px;
            font-weight:bold;
            border:none;
        """)

        # Clock Styling
        self.clock.setStyleSheet("""
            color:#00E5FF;
            font-size:16px;
            font-weight:bold;
            border:none;
        """)

        # Close Button Styling
        self.close_btn.setStyleSheet("""
            QPushButton {
                color:#FF4444;
                font-size:18px;
                font-weight:bold;
                background:transparent;
                border:none;
                padding:5px;
            }
            QPushButton:hover {
                color:#FF0000;
                background:#22FF4444;
                border-radius:4px;
            }
        """)

        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.status)
        layout.addSpacing(20)
        layout.addWidget(self.clock)
        layout.addSpacing(15)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

        # Close button event listener
        self.close_btn.clicked.connect(
            self.close_application
        )

        # Live Clock Setup
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()

    def update_clock(self):
        current = QTime.currentTime()
        self.clock.setText(
            current.toString("hh:mm:ss")
        )

    def close_application(self):
        if self.window():
            self.window().close()