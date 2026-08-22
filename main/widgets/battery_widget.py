import psutil
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar

from main.styles.theme import Theme


class BatteryWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label.setStyleSheet("""
            QLabel{
                color:white;
                font-size:16px;
                font-weight:bold;
                border:none;
            }
        """)

        self.bar = QProgressBar()
        self.bar.setMaximum(100)
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(8)

        self.bar.setStyleSheet("""
            QProgressBar{
                background:#2A2A2A;
                border:none;
                border-radius:5px;
            }

            QProgressBar::chunk{
                background:#00FF99;
                border-radius:5px;
            }
        """)

        layout.addWidget(self.label)
        layout.addWidget(self.bar)

        self.setStyleSheet(f"""
            QWidget{{
                background:#08111F;
                border:2px solid {Theme.BORDER};
                border-radius:12px;
            }}
        """)
        self.setFixedHeight(52)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_battery)
        self.timer.start(3000)

        self.update_battery()

    def update_battery(self):

        battery = psutil.sensors_battery()

        if battery is None:
            self.label.setText("🔋 Battery : N/A")
            self.bar.setValue(0)
            return

        percent = int(battery.percent)

        self.bar.setValue(percent)

        if battery.power_plugged:
            icon = "⚡"
            color = "#00FF99"

        elif percent >= 60:
            icon = "🟢"
            color = "#00FF99"

        elif percent >= 30:
            icon = "🟡"
            color = "#FFC107"

        else:
            icon = "🔴"
            color = "#FF3B30"

        self.label.setText(f"{icon} Battery : {percent}%")

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