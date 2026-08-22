from PyQt6.QtCore import QObject, QTimer


class DemoState(QObject):

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.states = [
            "IDLE",
            "LISTENING",
            "THINKING",
            "SPEAKING",
            "IDLE",
            "ERROR",
        ]

        self.index = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_state)
        self.timer.start(3000)   # हर 3 सेकंड में State बदलेगी

    def next_state(self):
        state = self.states[self.index]
        self.controller.set_state(state)

        # Step 26: State के हिसाब से Dynamic Message भेजना
        messages = {
            "IDLE": "Waiting for command...",
            "LISTENING": "Listening...",
            "THINKING": "Thinking...",
            "SPEAKING": "Speaking...",
            "ERROR": "Something went wrong!"
        }
        self.controller.set_message(
            messages[state]
        )

        self.index += 1

        if self.index >= len(self.states):
            self.index = 0