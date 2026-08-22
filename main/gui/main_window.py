from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt

from main.gui.top_bar import TopBar
from main.gui.left_panel import LeftPanel
from main.gui.center_panel import CenterPanel
from main.gui.right_panel import RightPanel
from main.gui.bottom_panel import BottomPanel


class MainWindow(QWidget):

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.setup_window()
        self.build_ui()

    def setup_window(self):
        self.setWindowTitle("Sanskari AI - JARVIS HUD")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.showMaximized()

        self.setStyleSheet("""
        QWidget{
            background:#05080F;
            color:white;
            font-family:Segoe UI;
        }
        """)

    def build_ui(self):

        main_layout = QVBoxLayout()

        # Top Bar
        main_layout.addWidget(TopBar())

        # Middle Layout
        middle_layout = QHBoxLayout()

        middle_layout.addWidget(LeftPanel())
        
        # Updated CenterPanel reference with controller passing
        self.center_panel = CenterPanel(self.controller)
        middle_layout.addWidget(self.center_panel, 1)

        middle_layout.addWidget(RightPanel())

        main_layout.addLayout(middle_layout)

        # Bottom Bar
        main_layout.addWidget(BottomPanel())

        self.setLayout(main_layout)