import asyncio
import speech_recognition as sr
import edge_tts
import pygame
import tempfile
from typing import Optional

class VoiceInterface:
    def __init__(self, settings):
        self.settings = settings
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.voice_name = settings.tts_voice  # Example: "en-US-AriaNeural"

        pygame.mixer.init()  # ✅ Add this line

    async def initialize(self):
        pygame.mixer.init()
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

    async def speech_to_text(self, audio_data) -> Optional[str]:
        try:
            text = self.recognizer.recognize_google(audio_data)
            return text.lower().strip()
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None

    async def text_to_speech(self, text: str):
        print("🗣 Speaking:", text)
        try:
            communicate = edge_tts.Communicate(text, self.voice_name)

            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        tmp_file.write(chunk["data"])

                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    await asyncio.sleep(0.1)

        except Exception as e:
            print(f"TTS error: {e}")

    async def listen_for_wake_word(self) -> bool:
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=2)
                text = await self.speech_to_text(audio)
                wake_words = ["hey nayraa", "nayraa", "hey nara"]
                return any(wake in text for wake in wake_words) if text else False
        except Exception:
            return False