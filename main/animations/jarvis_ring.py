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

    def animate(self):

        if self.state == "IDLE":
            outer_speed = 1
            inner_speed = -2
            radar_speed = 1

        elif self.state == "LISTENING":
            outer_speed = 3
            inner_speed = -4
            radar_speed = 2

        elif self.state == "THINKING":
            outer_speed = 5
            inner_speed = -6
            radar_speed = 4

        elif self.state == "SPEAKING":
            outer_speed = 4
            inner_speed = -5
            radar_speed = 3

        elif self.state == "ERROR":
            outer_speed = 0
            inner_speed = 0
            radar_speed = 0

        