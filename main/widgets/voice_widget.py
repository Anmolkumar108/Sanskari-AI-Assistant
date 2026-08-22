from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar

from main.styles.theme import Theme


class VoiceWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 5, 8, 5)
        layout.setSpacing(2)

        # -----------------------------
        # Label
        # -----------------------------

        self.label = QLabel("🔊 Volume : 0%")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label.setStyleSheet("""
            QLabel{
                color:white;
                font-size:15px;
                font-weight:bold;
                border:none;
            }
        """)

        # -----------------------------
        # Progress Bar
        # -----------------------------

        self.bar = QProgressBar()
        self.bar.setMaximum(100)
        self.bar.setValue(0)
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(7)

        self.bar.setStyleSheet("""
            QProgressBar{
                background:#2A2A2A;
                border:none;
                border-radius:5px;
            }

            QProgressBar::chunk{
                background:#1DA1F2;
                border-radius:5px;
            }
        """)

        layout.addWidget(self.label)
        layout.addWidget(self.bar)

        # -----------------------------
        # Card Style
        # -----------------------------

        self.setStyleSheet(f"""
            QWidget{{
                border:1px solid {Theme.BORDER};
                border-radius:10px;
                background:transparent;
            }}
        """)

        self.setFixedHeight(52)

    # =====================================================
    # Update Volume
    # =====================================================

    def update_volume(self, value):

        # Agar value string ho (jaise "21%")
        if isinstance(value, str):
            value = value.replace("%", "").strip()

        try:
            value = int(value)
        except Exception:
            value = 0

        value = max(0, min(100, value))

        self.bar.setValue(value)

        if value == 0:
            icon = "🔇"
            color = "#808080"

        elif value < 40:
            icon = "🔉"
            color = "#1DA1F2"

        elif value < 80:
            icon = "🔊"
            color = "#00E5FF"

        else:
            icon = "📢"
            color = "#00FF99"

        self.label.setText(f"{icon} Volume : {value}%")

        self.bar.setStyleSheet(f"""
            QProgressBar{{
                background:#2A2A2A;
                border:none;
                border-radius:5px;
            }}

            QProgressBar::chunk{{
                background:{color};
                border-radius:5px;
            }}
        """)