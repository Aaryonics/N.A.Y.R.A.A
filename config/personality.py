class PersonalityEngine:
    def __init__(self, settings):
        self.settings = settings

    def build_prompt(self, user_input, context):
        name = context.get("facts", {}).get("name", "User")
        history = context.get("history", [])
        convo = "\n".join([f"User: {x['user']}\nNayraa: {x['ai']}" for x in history])
        
        personality_prefix = (
            f"You are Nayraa, an intelligent and confident AI assistant. "
            f"You are witty, calm, helpful, and sometimes lightly tease the user in a friendly way. "
            f"The user's name is {name}. Always reply with a confident tone."
        )

        return f"{personality_prefix}\n\n{convo}\nUser: {user_input}\nNayraa:"

    def apply_personality_filter(self, response, context):
        # Later: you can modify tone, inject taunts, emojis, etc.
        return response.strip()
