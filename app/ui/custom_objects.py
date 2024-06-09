from PyQt5.QtCore import (
    QEasingCurve,
    QEvent,
    QPropertyAnimation,
    Qt,
    pyqtProperty,
    pyqtSignal,
)
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QLabel, QPushButton


class AnimationShadowEffect(QGraphicsDropShadowEffect):

    def __init__(self, color, *args, **kwargs):
        super(AnimationShadowEffect, self).__init__(*args, **kwargs)
        self.setColor(color)
        self.setOffset(0, 0)
        self.setBlurRadius(0)
        self._radius = 0
        self.animation = QPropertyAnimation(self)
        self.animation.setTargetObject(self)
        self.animation.setLoopCount(-1)
        self.animation.setDuration(2000)
        self.animation.setPropertyName(b"radius")
        self.animation.setEasingCurve(QEasingCurve.OutInBack)
        self.animation.setKeyValueAt(0.1, 1)
        self.animation.setKeyValueAt(0.5, 30)
        self.animation.setKeyValueAt(1, 1)

    def start(self):
        self.animation.start()

    def stop(self, r=0):
        self.radius = r
        self.animation.stop()

    @pyqtProperty(int)
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, r):
        self._radius = r
        self.setBlurRadius(r)


class PushButton(QPushButton):
    hover = pyqtSignal(str)

    def __init__(self, parent=None):
        super(PushButton, self).__init__(parent)
        pass

    def enterEvent(self, event):
        self.hover.emit("enterEvent")

    def leaveEvent(self, event):
        self.hover.emit("leaveEvent")


class ClickableLabel(QLabel):

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)
        self.setWordWrap(True)

    clicked = pyqtSignal()
    redirect = pyqtSignal()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        elif event.button() == Qt.MouseButton.RightButton:
            self.redirect.emit()
