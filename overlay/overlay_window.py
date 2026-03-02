import ctypes
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt


class Overlay(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # -------------------------------
        # 기본 윈도우 설정
        # -------------------------------
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        # ★ Windows 레벨 클릭 완전 통과 설정 ★
        self.make_click_through()

        self._rects = []
        self.hide()

    # ---------------------------------------
    # Windows 전용 클릭 완전 통과 처리
    # ---------------------------------------
    def make_click_through(self):
        hwnd = self.winId().__int__()

        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 0x00080000
        WS_EX_TRANSPARENT = 0x00000020

        user32 = ctypes.windll.user32
        style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style | WS_EX_LAYERED | WS_EX_TRANSPARENT
        user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

    # ---------------------------------------
    # 오버레이 표시
    # ---------------------------------------
    def show_for_game_region(self, game_rect, rects):
        left, top, right, bottom = game_rect
        width = right - left
        height = bottom - top

        self.setGeometry(left, top, width, height)

        self._rects = rects

        if self._rects:
            self.show()
            self.update()
        else:
            self.hide()

    def clear(self):
        self._rects = []
        self.hide()

    # ---------------------------------------
    # 실제 그리기
    # ---------------------------------------
    def paintEvent(self, event):

        if not self._rects:
            return

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        for (x, y, w, h, text) in self._rects:

            painter.fillRect(x, y, w, h, QtGui.QColor(0, 0, 0, 150))

            pen = QtGui.QPen(QtGui.QColor(255, 215, 0))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawRect(x, y, w, h)

        painter.end()