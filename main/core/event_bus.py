from PyQt6.QtCore import QObject, pyqtSignal


class EventBus(QObject):

    # AI
    state_changed = pyqtSignal(str)
    message_received = pyqtSignal(str)

    # Logs
    log_message = pyqtSignal(str)

    # Chat
    chat_message = pyqtSignal(str)

    # NEW Chat Signals
    user_message = pyqtSignal(str)
    assistant_message = pyqtSignal(str)

    # Voice
    voice_level = pyqtSignal(int)

    # Tool
    tool_started = pyqtSignal(str)
    tool_finished = pyqtSignal(str)
    tool_changed = pyqtSignal(str)
    tool_icon_changed = pyqtSignal(str)
    tool_status_changed = pyqtSignal(str)

    # Command
    last_command_changed = pyqtSignal(str)

    # Response
    response_changed = pyqtSignal(str)

    # Weather
    weather_changed = pyqtSignal(str)

    # Internet
    internet_changed = pyqtSignal(str)

    # Mic
    mic_changed = pyqtSignal(str)

    # Connection
    connection_changed = pyqtSignal(str)

    # Agent
    agent_online = pyqtSignal()
    agent_offline = pyqtSignal()

    # ==========================
    # System Monitor
    # ==========================

    cpu_changed = pyqtSignal(str)
    ram_changed = pyqtSignal(str)
    battery_changed = pyqtSignal(str)
    disk_changed = pyqtSignal(str)
    network_changed = pyqtSignal(str)
    volume_changed = pyqtSignal(str)

    # Notification
    notification = pyqtSignal(str)

    def __init__(self):
        super().__init__()


event_bus = EventBus()