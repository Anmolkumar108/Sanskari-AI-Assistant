from main.core.ai_controller import AIController
from main.core.event_bus import event_bus
from main.core.tool_manager import ToolManager


class AIBridge:

    def __init__(self, controller: AIController):
        self.controller = controller

    # -------------------------
    # STATE
    # -------------------------

    def set_state(self, state):

        self.controller.set_state(state)

    # -------------------------
    # MESSAGE
    # -------------------------

    def set_message(self, message):

        self.controller.set_message(message)

    # -------------------------
    # LOG
    # -------------------------

    def log(self, message):

        event_bus.log_message.emit(message)

    # -------------------------
    # CHAT
    # -------------------------

    def chat(self, message):

        event_bus.chat_message.emit(message)

    # -------------------------
    # TOOL EVENTS
    # -------------------------

    def tool_started(self, tool):

        ToolManager.start(tool)

        event_bus.tool_started.emit(tool)

        self.log(f"Tool Started : {tool}")

    def tool_finished(self, tool):

        ToolManager.finish()

        event_bus.tool_finished.emit(tool)

        self.log(f"Tool Finished : {tool}")

    # -------------------------
    # CONNECTION
    # -------------------------

    def online(self):

        event_bus.agent_online.emit()

        self.log("Agent Connected")

    def offline(self):

        event_bus.agent_offline.emit()

        self.log("Agent Disconnected")

    # -------------------------
    # SHORTCUTS
    # -------------------------

    def on_idle(self):

        self.set_state("IDLE")

        self.set_message("Waiting for command...")

    def on_listening(self):

        self.set_state("LISTENING")

        self.set_message("Listening...")

    def on_thinking(self):

        self.set_state("THINKING")

        self.set_message("Thinking...")

    def on_speaking(self):

        self.set_state("SPEAKING")

        self.set_message("Speaking...")

    def on_error(self, msg="Unknown Error"):

        self.set_state("ERROR")

        self.set_message(msg)

        self.log(msg)