from PyQt5 import QtWidgets, QtCore, QtGui


class Overlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.gray_rects = []

    def clear_overlays(self):
        self.gray_rects = []
        self.update()

    def add_gray_rect(self, x, y, w, h):
        self.gray_rects.append((x, y, w, h))
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        for rect in self.gray_rects:
            x, y, w, h = rect
            painter.fillRect(
                x, y, w, h,
                QtGui.QColor(0, 0, 0, 150)  # 반투명 검정
            )