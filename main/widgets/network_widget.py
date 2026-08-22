from PyQt6.QtWidgets import QLabel
from main.core.event_bus import event_bus
from main.styles.theme import Theme


class NetworkWidget(QLabel):

    def __init__(self):
        super().__init__()

        self.setText("🌐 Network : 0 KB/s")

        self.setStyleSheet(f"""
            QLabel{{
                background:#091525;
                border:2px solid {Theme.BORDER};
                border-radius:10px;
                color:{Theme.SUCCESS};
                font-size:16px;
                font-weight:bold;
                padding:10px;
            }}
        """)

        event_bus.network_changed.connect(self.update_network)

    def update_network(self, speed):
        self.setText(f"🌐 {speed}")