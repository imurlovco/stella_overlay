import json
import os

CONFIG_PATH = os.path.join("config", "potential_data.json")

class SettingsManager:
    def __init__(self):
        self.data = {}
        self.current_character = None
        self.load()

    def load(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                self.data = json.load(f)

    def save(self):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def add_character(self, name):
        if name not in self.data:
            self.data[name] = {
                "main": {},
                "rare": {},
                "common": {}
            }
            self.save()

    def set_current_character(self, name):
        self.current_character = name

    def get_current_data(self):
        return self.data.get(self.current_character, {})

    def add_potential(self, tier, name):
        if name not in self.data[self.current_character][tier]:
            self.data[self.current_character][tier][name] = False
            self.save()

    def set_checked(self, tier, name, state):
        self.data[self.current_character][tier][name] = state
        self.save()

    def is_checked(self, name):
        current = self.get_current_data()
        for tier in ["main", "rare", "common"]:
            if name in current.get(tier, {}):
                return current[tier][name]
        return False