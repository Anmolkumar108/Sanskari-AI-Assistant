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

    def draw_core(self, painter):
        cx = self.width() / 2
        cy = self.height() / 2
        ring_color = self.get_ring_color()

        # Center Core Ellipse (Pulsing)
        painter.setBrush(QColor(ring_color))
        painter.setPen(Qt.PenStyle.NoPen)

        size = 56 + self.pulse
        painter.drawEllipse(
            int(cx - size / 2),
            int(cy - size / 2),
            int(size),
            int(size)
        )

        # Crosshair Lines
        pen = QPen(QColor(ring_color))
        pen.setWidth(2)
        painter.setPen(pen)

        # Horizontal Line
        painter.drawLine(
            int(cx - 25),
            int(cy),
            int(cx + 25),
            int(cy)
        )

        # Vertical Line
        painter.drawLine(
            int(cx),
            int(cy - 25),
            int(cx),
            int(cy + 25)
        )

    def draw_orbits(self, painter):
        cx = self.width() / 2
        cy = self.height() / 2
        ring_color = self.get_ring_color()

        # Outer Rotating Dot
        r = 140
        x = cx + math.cos(math.radians(self.outer_angle)) * r
        y = cy + math.sin(math.radians(self.outer_angle)) * r

        painter.setBrush(QColor(ring_color))
        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawEllipse(
            int(x - 7),
            int(y - 7),
            14,
            14
        )

        # Inner Rotating Dot
        r = 90
        x = cx + math.cos(math.radians(self.inner_angle)) * r
        y = cy + math.sin(math.radians(self.inner_angle)) * r

        painter.drawEllipse(
            int(x - 5),
            int(y - 5),
            10,
            10
        )

    def draw_ticks(self, painter, cx, cy, ring_color):
        pen = QPen(QColor(ring_color))
        pen.setWidth(2)

        painter.setPen(pen)

        radius = 155

        for angle in range(0, 360, 6):
            rad = math.radians(angle)

            x1 = cx + math.cos(rad) * radius
            y1 = cy + math.sin(rad) * radius

            x2 = cx + math.cos(rad) * (radius + 8)
            y2 = cy + math.sin(rad) * (radius + 8)

            painter.drawLine(
                int(x1),
                int(y1),
                int(x2),
                int(y2)
            )

    def draw_radar(self, painter, cx, cy, ring_color):
        pen = QPen(QColor(ring_color))
        pen.setWidth(6)

        painter.setPen(pen)

        rect_x = int(cx - 125)
        rect_y = int(cy - 125)
        rect_w = 250
        rect_h = 250

        painter.drawArc(
            rect_x,
            rect_y,
            rect_w,
            rect_h,
            -self.radar_angle * 16,
            -35 * 16
        )

    def draw_particles(self, painter):
        pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        cx = self.width() / 2
        cy = self.height() / 2
        ring_color = self.get_ring_color()

        self.draw_glow(painter, cx, cy, ring_color)
        self.draw_ticks(painter, cx, cy, ring_color)
        self.draw_outer_ring(painter)
        self.draw_radar(painter, cx, cy, ring_color)
        self.draw_inner_ring(painter)
        self.draw_orbits(painter)
        self.draw_core(painter)
        self.draw_particles(painter)