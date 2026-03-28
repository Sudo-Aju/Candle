import json
import os

class ConfigManager:
    """Manages saving and loading engine configurations."""
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.default_config = {
            "SCREEN_WIDTH": 800,
            "SCREEN_HEIGHT": 600,
            "FPS": 60,
            "MIC_THRESHOLD": 700,
            "BLOW_LIMIT": 1.5
        }
        self.settings = self.load_config()

    def load_config(self):
        if not os.path.exists(self.filename):
            self.save_config(self.default_config)
            return self.default_config
        with open(self.filename, 'r') as f:
            return json.load(f)

    def save_config(self, data=None):
        if data is None:
            data = self.settings
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)