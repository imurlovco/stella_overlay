import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

from core.window_tracker import get_window_rect
from core.capture import capture_region
from core.ocr_engine import extract_text
from overlay.overlay_window import Overlay
from ui.settings_ui import SettingsUI

# 게임 창 제목 (반드시 실제 창 제목과 동일해야 함)
GAME_TITLE = "StellaSora"

# 타이머 간격
UPDATE_INTERVAL_MS = 400


# 🔥 1920x1080 기준 카드 고정 좌표 (게임 내부 좌표계)
CARD_POSITIONS_1920 = [
    (380, 330, 350, 520),
    (785, 330, 350, 520),
    (1190, 330, 350, 520),
]


def scale_card_positions(base_positions, game_w, game_h):
    """
    1920x1080 기준 좌표를
    현재 게임 해상도에 맞게 자동 스케일링
    """
    scale_x = game_w / 1920
    scale_y = game_h / 1080

    scaled = []
    for (x, y, w, h) in base_positions:
        scaled.append((
            int(x * scale_x),
            int(y * scale_y),
            int(w * scale_x),
            int(h * scale_y)
        ))
    return scaled


def main():
    app = QtWidgets.QApplication(sys.argv)

    settings_ui = SettingsUI()
    settings_ui.show()

    manager = settings_ui.manager
    overlay = Overlay()

    overlay_enabled = {"value": True}

    # F8 오버레이 토글
    shortcut = QShortcut(QKeySequence("F8"), settings_ui)

    def toggle_overlay():
        overlay_enabled["value"] = not overlay_enabled["value"]
        if not overlay_enabled["value"]:
            overlay.clear()
        settings_ui.setWindowTitle(
            f"잠재력 설정 - Overlay {'ON' if overlay_enabled['value'] else 'OFF'}"
        )

    shortcut.activated.connect(toggle_overlay)

    def update():
        rect = get_window_rect(GAME_TITLE)

        if not rect:
            overlay.clear()
            return

        left, top, right, bottom = rect
        game_w = right - left
        game_h = bottom - top

        frame = capture_region(rect)
        if frame is None:
            overlay.clear()
            return

        # 현재 해상도에 맞게 카드 좌표 스케일링
        card_positions = scale_card_positions(
            CARD_POSITIONS_1920,
            game_w,
            game_h
        )

        overlay_rects = []

        for i, (x, y, w, h) in enumerate(card_positions):

            # 카드 영역만 잘라서 OCR
            card_img = frame[y:y + h, x:x + w]

            try:
                text = extract_text(card_img).strip()
            except Exception:
                text = ""

            # 텍스트가 너무 짧거나 이상하면 무시 (OCR 노이즈 제거)
            if len(text) < 2:
                continue

            checked = manager.is_checked(text)

            # 체크 안 된 카드만 덮음
            if not checked and overlay_enabled["value"]:
                overlay_rects.append((x, y, w, h, None))

        if overlay_rects and overlay_enabled["value"]:
            overlay.show_for_game_region(rect, overlay_rects)
        else:
            overlay.clear()

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(UPDATE_INTERVAL_MS)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()