from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox,
    QComboBox, QPushButton, QScrollArea,
    QLineEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt
from core.settings_manager import SettingsManager


class SettingsUI(QWidget):
    def __init__(self):
        super().__init__()

        self.manager = SettingsManager()
        self.setWindowTitle("잠재력 설정")
        self.resize(400, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 캐릭터 선택 드롭다운
        self.character_dropdown = QComboBox()
        self.character_dropdown.addItems(self.manager.data.keys())
        self.character_dropdown.currentTextChanged.connect(self.change_character)
        self.layout.addWidget(self.character_dropdown)

        # 캐릭터 추가 영역
        add_layout = QHBoxLayout()
        self.new_character_input = QLineEdit()
        self.new_character_input.setPlaceholderText("새 캐릭터 이름")
        add_btn = QPushButton("캐릭터 추가")
        add_btn.clicked.connect(self.add_character)
        add_layout.addWidget(self.new_character_input)
        add_layout.addWidget(add_btn)
        self.layout.addLayout(add_layout)

        # 스크롤 영역
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll)

        if self.manager.data:
            first_char = list(self.manager.data.keys())[0]
            self.manager.set_current_character(first_char)
            self.load_potentials()

    def add_character(self):
        name = self.new_character_input.text().strip()
        if name:
            self.manager.add_character(name)
            self.character_dropdown.addItem(name)
            self.new_character_input.clear()

    def change_character(self, name):
        self.manager.set_current_character(name)
        self.load_potentials()

    def clear_layout(self):
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def load_potentials(self):
        self.clear_layout()
        data = self.manager.get_current_data()

        for tier in ["main", "rare", "common"]:
            title = QLabel(f"--- {tier.upper()} ---")
            title.setAlignment(Qt.AlignCenter)
            self.scroll_layout.addWidget(title)

            for name, state in data.get(tier, {}).items():
                checkbox = QCheckBox(name)
                checkbox.setChecked(state)
                checkbox.stateChanged.connect(
                    lambda s, t=tier, n=name:
                    self.manager.set_checked(t, n, s == 2)
                )
                self.scroll_layout.addWidget(checkbox)

        self.scroll_layout.addStretch()