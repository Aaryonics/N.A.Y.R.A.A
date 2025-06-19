import json
from pathlib import Path
from datetime import datetime

class MemoryManager:
    def __init__(self, settings):
        self.settings = settings
        self.profile_path = settings.profile_path
        self.user_profile = {
            "name": "User",
            "facts": {},
            "conversations": []
        }

    async def load_user_profile(self):
        if Path(self.profile_path).exists():
            with open(self.profile_path, "r") as f:
                self.user_profile = json.load(f)
        else:
            self.save_user_profile()

    def save_user_profile(self):
        with open(self.profile_path, "w") as f:
            json.dump(self.user_profile, f, indent=2)

    async def store_conversation(self, user_input, response):
        self.user_profile["conversations"].append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "nayraa": response
        })
        self.save_user_profile()

    def get_recent_conversations(self, limit=3):
        return self.user_profile["conversations"][-limit:]

    def get_user_facts(self):
        return self.user_profile.get("facts", {})

    def update_fact(self, key, value):
        self.user_profile["facts"][key] = value
        self.save_user_profile()
