import asyncio

from core.voice_interface import VoiceInterface
from core.llm_client import LLMClient
from core.context_manager import ContextManager
from memory.memory_manager import MemoryManager
from config.personality import PersonalityEngine

class NayraaEngine:
    def __init__(self, settings):
        self.settings = settings
        self.voice = VoiceInterface(settings)
        self.llm = LLMClient(settings)
        self.context = ContextManager()
        self.memory = MemoryManager(settings)
        self.personality = PersonalityEngine(settings)

        self.is_listening = False
        self.is_speaking = False
        self.wake_word_detected = False

    async def generate_response(self, user_input, context={}):
        prompt = self.personality.build_prompt(user_input, context)
        print("🧠 Final prompt to LLM:\n", prompt)
        response = await self.llm.generate_response(prompt)
        print("🧠 Raw LLM response:", response)

    async def initialize(self):
        await self.voice.initialize()
        await self.llm.initialize()
        await self.memory.load_user_profile()

    async def generate_response(self, user_input, context={}):
        prompt = self.personality.build_prompt(user_input, context)
        response = await self.llm.generate_response(prompt)
        response = self.personality.apply_personality_filter(response, context)
        return response

    async def process_voice_input(self, audio_data):
        try:
            user_input = await self.voice.speech_to_text(audio_data)
            if not user_input:
                return None
            context = await self.context.build_context(user_input, self.memory)
            response = await self.generate_response(user_input, context)
            await self.memory.store_conversation(user_input, response)
            return response
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

    async def speak_response(self, text):
        self.is_speaking = True
        try:
            await self.voice.text_to_speech(text)
        finally:
            self.is_speaking = False

    async def run(self):
        # You can implement a loop here for continuous listening
        pass


   

