import json
from pathlib import Path

class Settings:
    def __init__(self):
        self.config_dir = Path.home() / ".nayraa"
        self.config_dir.mkdir(exist_ok=True)

        self.config_file = self.config_dir / "config.json"
        self.profile_path = self.config_dir / "user_profile.json"
        self.database_path = self.config_dir / "conversations.db"
        self.api_key: str = "AIzaSyAr9a0GFYXRPET-_erOTI4SzQE-0Sku7ys"
        self.llm_provider: str = "google"
        self.llm_model: str = "gemini-1.5-flash-latest"

        # Default config values
        self.defaults = {
            "tts_provider": "edge",
            "tts_voice": "en-US-AriaNeural",    # ✅ <--- THIS is where tts_voice is set
            "wake_word_enabled": True,
            "start_minimized": False,
            "auto_start": False,
            "voice_activation_threshold": 0.5,
            "personality_adaptation_rate": 0.1
        }

        # Load or initialize config
        self.load_settings()

    def load_settings(self):
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}

        # Use default values if not found
        for key, default in self.defaults.items():
            value = config.get(key, default)
            setattr(self, key, value)

        # Save config with missing values filled in
        self.save_settings()

    def save_settings(self):
        config = {key: getattr(self, key, self.defaults[key]) for key in self.defaults}
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

