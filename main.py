import sys
from PyQt5 import QtWidgets, QtCore
from core.window_tracker import get_window_rect
from core.capture import capture_region
from core.card_detector import split_into_cards
from core.ocr_engine import extract_text
from core.settings_manager import SettingsManager
from overlay.overlay_window import Overlay
from ui.settings_ui import SettingsUI

GAME_TITLE = "StellaSora"


def main():
    app = QtWidgets.QApplication(sys.argv)

    overlay = Overlay()
    overlay.show()

    settings_ui = SettingsUI()
    settings_ui.show()

    manager = settings_ui.manager

    def update():
        rect = get_window_rect(GAME_TITLE)
        if not rect:
            return

        overlay.setGeometry(rect[0], rect[1],
                            rect[2] - rect[0],
                            rect[3] - rect[1])

        frame = capture_region(rect)
        cards = split_into_cards(frame)

        overlay.clear_overlays()

        card_width = (rect[2] - rect[0]) // 3
        card_height = rect[3] - rect[1]

        for i, card in enumerate(cards):
            text = extract_text(card).strip()

            if not manager.is_checked(text):
                x = i * card_width
                overlay.add_gray_rect(x, 0, card_width, card_height)

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(500)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()