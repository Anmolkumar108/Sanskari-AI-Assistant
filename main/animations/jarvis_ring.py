import math
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import (
    QPainter,
    QColor,
    QPen,
    QRadialGradient,
    QBrush,
    QPainterPath,
)
from PyQt6.QtWidgets import QWidget


class JarvisRing(QWidget):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(420, 420)

        self.state = "IDLE"

        self.outer_angle = 0
        self.inner_angle = 0
        self.radar_angle = 0

        self.pulse = 0
        self.pulse_direction = 1

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

    def set_state(self, state):
        self.state = state
        self.update()

    