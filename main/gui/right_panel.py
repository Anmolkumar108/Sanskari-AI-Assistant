from PyQt6.QtWidgets import QLabel

from main.gui.components.hud_panel import HudPanel
from main.core.event_bus import event_bus


class RightPanel(HudPanel):

    def __init__(self):
        super().__init__()

        self.setFixedWidth(300)

        # =========================
        # TITLE
        # =========================

        title = QLabel("SYSTEM")

        title.setStyleSheet("""
            color:#00E5FF;
            font-size:24px;
            font-weight:bold;
            background:transparent;
        """)

        self.layout.addWidget(title)

        self.layout.addSpacing(25)

        # =========================
        # AGENT STATUS (Member Variables)
        # =========================

        self.agent = QLabel("Agent : 🔴 Offline")
        self.tool = QLabel("Tool : None")
        self.tool_status = QLabel("Status : Idle")
        self.tool_icon = QLabel("Icon : ⚪")
        self.command = QLabel("Last Command : -")
        self.response = QLabel("Response : Ready")
        self.internet = QLabel("Internet : Connected")
        self.weather = QLabel("Weather : --")
        self.mic = QLabel("Mic : Active")

        # =========================
        # SYSTEM MONITOR
        # =========================

        self.cpu = QLabel("CPU : 0%")
        self.ram = QLabel("RAM : 0%")
        self.disk = QLabel("Disk : 0%")
        # self.battery = QLabel("Battery : N/A")
        # self.volume = QLabel("Volume : 0%")

        labels = [
            self.agent,
            self.tool,
            self.tool_status,
            self.tool_icon,
            self.command,
            self.response,
            self.internet,
            self.weather,
            self.mic,
            self.cpu,
            self.ram,
            self.disk,
            # self.battery,
            # self.volume,
        ]

        for label in labels:

            label.setStyleSheet("""
                color:white;
                font-size:16px;
                background:transparent;
                padding:6px;
            """)

            self.layout.addWidget(label)

        self.layout.addStretch()

        # =========================
        # EVENT BUS CONNECTIONS
        # =========================

        event_bus.agent_online.connect(
            lambda: (
                print("GUI : ONLINE"),
                self.agent.setText("Agent : 🟢 Online")
            )
        )

        event_bus.agent_offline.connect(
            lambda: (
                print("GUI : OFFLINE"),
                self.agent.setText("Agent : 🔴 Offline")
            )
        )

        event_bus.tool_changed.connect(
            lambda x: self.tool.setText(
                f"Tool : {x}"
            )
        )

        event_bus.tool_status_changed.connect(
            lambda x: self.tool_status.setText(
                f"Status : {x}"
            )
        )

        event_bus.tool_icon_changed.connect(
            lambda x: self.tool_icon.setText(
                f"Icon : {x}"
            )
        )

        event_bus.last_command_changed.connect(
            lambda x: self.command.setText(
                f"Last Command : {x}"
            )
        )

        event_bus.response_changed.connect(
            lambda x: self.response.setText(
                f"Response : {x}"
            )
        )

        event_bus.internet_changed.connect(
            lambda x: self.internet.setText(
                f"Internet : {x}"
            )
        )

        # =========================
        # WEATHER EVENT CONNECTION
        # =========================
        event_bus.weather_changed.connect(
            lambda x: self.weather.setText(
                f"Weather : {x}"
            )
        )

        event_bus.mic_changed.connect(
            lambda x: self.mic.setText(
                f"Mic : {x}"
            )
        )

        event_bus.cpu_changed.connect(
            lambda x: self.cpu.setText(f"CPU : {x}")
        )

        event_bus.ram_changed.connect(
            lambda x: self.ram.setText(f"RAM : {x}")
        )

        event_bus.disk_changed.connect(
            lambda x: self.disk.setText(f"Disk : {x}")
        )

        # event_bus.battery_changed.connect(
        #     lambda x: self.battery.setText(f"Battery : {x}")
        # )

        # event_bus.volume_changed.connect(
        #     lambda x: self.volume.setText(f"Volume : {x}")
        # )