from ctypes import POINTER, cast
import psutil
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from PyQt6.QtCore import QObject, QTimer

from main.core.event_bus import event_bus


class SystemMonitor(QObject):

    def __init__(self):
        super().__init__()

        # Network speed tracking variables
        self.last_net_io = psutil.net_io_counters()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def update(self):
        try:
            # CPU, RAM, Disk
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage("/").percent

            # Battery
            battery = psutil.sensors_battery()
            if battery:
                battery_str = f"{battery.percent}%"
            else:
                battery_str = "N/A"

            # -----------------------------
            # Volume
            # -----------------------------
            try:
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(
                    IAudioEndpointVolume._iid_,
                    CLSCTX_ALL,
                    None,
                )
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                current = volume.GetMasterVolumeLevelScalar()
                volume_percent = int(current * 100)
            except Exception:
                volume_percent = 0

            # -----------------------------
            # Network Speed
            # -----------------------------
            try:
                net_io = psutil.net_io_counters()
                bytes_sent = net_io.bytes_sent - self.last_net_io.bytes_sent
                bytes_recv = net_io.bytes_recv - self.last_net_io.bytes_recv
                self.last_net_io = net_io

                # Convert to KB/s or MB/s for clean display
                def format_speed(bytes_sec):
                    kb = bytes_sec / 1024
                    if kb >= 1024:
                        return f"{kb / 1024:.1f} MB/s"
                    return f"{int(kb)} KB/s"

                net_speed = f"↓ {format_speed(bytes_recv)} | ↑ {format_speed(bytes_sent)}"
            except Exception:
                net_speed = "0 KB/s"

            # Emit all signals
            event_bus.cpu_changed.emit(f"{cpu}%")
            event_bus.ram_changed.emit(f"{ram}%")
            event_bus.disk_changed.emit(f"{disk}%")
            event_bus.battery_changed.emit(battery_str)
            event_bus.volume_changed.emit(f"{volume_percent}%")
            event_bus.network_changed.emit(net_speed)

        except Exception as e:
            print("System Monitor Error:", e)