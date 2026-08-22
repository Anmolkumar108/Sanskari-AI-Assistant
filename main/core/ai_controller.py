from PyQt6.QtCore import QObject, pyqtSignal
from main.core.event_bus import event_bus


class AIController(QObject):

    state_changed = pyqtSignal(str)
    message_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.state = "IDLE"
        self.message = "Ready"

    def set_state(self, state):

        self.state = state

        self.state_changed.emit(state)
        event_bus.state_changed.emit(state)

    def set_message(self, message):

        self.message = message

        self.message_changed.emit(message)
        event_bus.message_received.emit(message)

    def get_state(self):
        return self.state

    def get_message(self):
        return self.message