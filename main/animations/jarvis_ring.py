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

        else:
            outer_speed = 2
            inner_speed = -3
            radar_speed = 1

        self.outer_angle += outer_speed
        self.inner_angle += inner_speed
        self.radar_angle += radar_speed

        self.outer_angle %= 360
        self.inner_angle %= 360
        self.radar_angle %= 360

        # Pulse Animation Logic
        self.pulse += self.pulse_direction
        if self.pulse >= 8:
            self.pulse_direction = -1
        elif self.pulse <= 0:
            self.pulse_direction = 1

        self.update()

    def draw_glow(self, painter, cx, cy, ring_color):

        gradient = QRadialGradient(cx, cy, 170)

        color = QColor(ring_color)
        color.setAlpha(70)
        gradient.setColorAt(0.0, color)

        transparent = QColor(ring_color)
        transparent.setAlpha(0)
        gradient.setColorAt(1.0, transparent)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(gradient))

        painter.drawEllipse(
            int(cx - 170),
            int(cy - 170),
            340,
            340
        )

    def get_ring_color(self):
        if self.state == "LISTENING":
            return "#00FF99"
        elif self.state == "THINKING":
            return "#FFD700"
        elif self.state == "SPEAKING":
            return "#FF4DFF"
        elif self.state == "ERROR":
            return "#FF4444"
        return "#00E5FF"

    def draw_outer_ring(self, painter):
        cx = self.width() / 2
        cy = self.height() / 2
        ring_color = self.get_ring_color()

        pen = QPen(QColor(ring_color))
        pen.setWidth(4)
        painter.setPen(pen)

        painter.drawEllipse(
            int(cx - 140),
            int(cy - 140),
            280,
            280
        )

    def draw_inner_ring(self, painter):
        cx = self.width() / 2
        cy = self.height() / 2
        ring_color = self.get_ring_color()

        pen = QPen(QColor(ring_color))
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawEllipse(
            int(cx - 90),
            int(cy - 90),
            180,
            180
        )

    