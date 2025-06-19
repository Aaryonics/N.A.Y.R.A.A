class ContextManager:
    def __init__(self):
        self.history = []

    async def build_context(self, user_input, memory):
        context = {}

        # Add recent messages
        recent = memory.get_recent_conversations(limit=3)
        context["history"] = recent

        # Add extracted facts (name, mood, etc.)
        context["facts"] = memory.get_user_facts()

        # Add last user input
        context["last_input"] = user_input

        return context

    def add_to_history(self, user_input, response):
        self.history.append({"user": user_input, "ai": response})
        if len(self.history) > 10:
            self.history.pop(0)
