from PyQt6.QtWidgets import QLabel

from main.gui.components.hud_panel import HudPanel
from main.core.event_bus import event_bus
from main.widgets.clock_widget import ClockWidget
from main.widgets.battery_widget import BatteryWidget
from main.widgets.voice_widget import VoiceWidget
from main.widgets.network_widget import NetworkWidget


class LeftPanel(HudPanel):

    def __init__(self):
        super().__init__()

        self.setFixedWidth(260)
        self.layout.setSpacing(6)

        # =========================
        # TITLE
        # =========================

        title = QLabel("SYSTEM STATUS")

        title.setStyleSheet("""
            color:#00E5FF;
            font-size:24px;
            font-weight:bold;
            background:transparent;
        """)

        self.layout.addWidget(title)

        # =========================
        # BATTERY WIDGET
        # =========================

        self.battery = BatteryWidget()
        self.layout.addWidget(self.battery)

        # =========================
        # VOICE / VOLUME WIDGET
        # =========================

        self.voice = VoiceWidget()
        self.layout.addWidget(self.voice)

        # =========================
        # NETWORK WIDGET
        # =========================

        self.network = NetworkWidget()
        self.layout.addWidget(self.network)

        self.layout.addSpacing(10)

        # =========================
        # AI INFO PANEL & LABELS
        # =========================

        info_panel = HudPanel()

        self.ai_name = QLabel("AI Name : Sanskari")
        self.ai_state = QLabel("State : IDLE")
        self.voice_label = QLabel("Voice : Aoede")
        self.model = QLabel("Model : Gemini")
        self.version = QLabel("Version : 3.0")
        self.connection = QLabel("Connection : Offline")

        labels = [
            self.ai_name,
            self.ai_state,
            self.voice_label,
            self.model,
            self.version,
            self.connection,
        ]

        for label in labels:
            label.setStyleSheet("""
                color:white;
                font-size:17px;
                background:transparent;
                padding:6px;
            """)
            info_panel.layout.addWidget(label)

        self.layout.addWidget(info_panel)

        # =========================
        # DATE & TIME
        # =========================

        self.layout.addSpacing(10)

        clock_title = QLabel("DATE & TIME")

        clock_title.setStyleSheet("""
            color:#00E5FF;
            font-size:18px;
            font-weight:bold;
            background:transparent;
        """)

        self.layout.addWidget(clock_title)

        self.clock = ClockWidget()

        self.layout.addWidget(self.clock)

        self.layout.addStretch()

        # =========================
        # EVENT BUS CONNECTIONS
        # =========================

        event_bus.state_changed.connect(
            lambda x: self.ai_state.setText(
                f"State : {x}"
            )
        )

        event_bus.connection_changed.connect(
            lambda x: self.connection.setText(
                f"Connection : {x}"
            )
        )

        event_bus.volume_changed.connect(
            self.voice.update_volume
        )