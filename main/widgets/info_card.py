from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

from main.styles.theme import Theme


class InfoCard(QWidget):

    def __init__(self, title: str, value: str):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)

        self.title = QLabel(title.upper())
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.title.setStyleSheet(f"""
            QLabel {{
                color:{Theme.TEXT_SECONDARY};
                font-size:11px;
                font-weight:bold;
                border:none;
                background:transparent;
            }}
        """)

        self.value = QLabel(value)
        self.value.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.value.setStyleSheet(f"""
            QLabel {{
                color:{Theme.TEXT};
                font-size:16px;
                font-weight:bold;
                border:none;
                background:transparent;
            }}
        """)

        layout.addWidget(self.title)
        layout.addWidget(self.value)

        self.setStyleSheet(f"""
            QWidget {{
                background:{Theme.CARD_BG};
                border:1px solid {Theme.BORDER};
                border-radius:8px;
            }}
        """)

    def setValue(self, text: str):
        self.value.setText(text)