from PyQt6.QtWidgets import QFrame, QVBoxLayout
from main.styles.theme import Theme


class HudPanel(QFrame):
    """
    Reusable HUD Panel
    """

    def __init__(self):
        super().__init__()

        self.setObjectName("HudPanel")

        self.setStyleSheet(f"""
        QFrame#HudPanel{{
            background-color:{Theme.PANEL_BG};
            border:2px solid {Theme.BORDER};
            border-radius:{Theme.PANEL_RADIUS}px;
        }}
        """)

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(15, 15, 15, 15)

        self.layout.setSpacing(10)

        self.setLayout(self.layout)