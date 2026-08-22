import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from main.gui.main_window import MainWindow
from main.core.ai_controller import AIController
from main.core.ai_bridge import AIBridge
from main.core.demo_state import DemoState
from main.core.agent_launcher import AgentLauncher
from main.core import assistant_events
from main.core.ipc.ipc_server import IPCServer
from main.core.event_bus import event_bus
from main.core.system_monitor import SystemMonitor
from main.core.tool_manager import ToolManager


app = QApplication(sys.argv)

controller = AIController()
bridge = AIBridge(controller)

# Assistant Events को Initialize किया गया
assistant_events.initialize(bridge)

# demo = DemoState(controller)

# IPC Server को पहले स्टार्ट किया गया फिर 1 सेकंड बाद Agent Launch किया गया
server = IPCServer()
server.start()

time.sleep(1)

launcher = AgentLauncher()
launcher.start()

monitor = SystemMonitor()

# =========================================
# Step 65: Phase-6 Real IPC Test
# =========================================
QTimer.singleShot(
    2000,
    lambda: event_bus.log_message.emit("IPC Server Started")
)
QTimer.singleShot(
    4000,
    lambda: controller.set_state("LISTENING")
)
QTimer.singleShot(
    6000,
    lambda: controller.set_state("THINKING")
)
QTimer.singleShot(
    8000,
    lambda: controller.set_state("SPEAKING")
)
QTimer.singleShot(
    10000,
    lambda: controller.set_state("IDLE")
)

# ToolManager Test
QTimer.singleShot(
    12000,
    lambda: ToolManager.start("weather")
)
QTimer.singleShot(
    17000,
    lambda: ToolManager.finish()
)

window = MainWindow(controller)

window.show()

event_bus.log_message.emit("GUI Started Successfully")

sys.exit(app.exec())