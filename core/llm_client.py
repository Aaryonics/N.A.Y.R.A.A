import asyncio
import google.generativeai as genai
from config.settings import Settings

settings: Settings = Settings()

# ✅ Configure Gemini API
genai.configure(api_key=settings.api_key)

class LLMClient:
    def __init__(self, settings):
        self.settings = settings
        self.provider = settings.llm_provider
        self.model = settings.llm_model
        self.api_key = settings.api_key

    async def initialize(self):
        # No setup needed for Gemini
        if self.provider != "google":
            raise NotImplementedError(f"LLM provider '{self.provider}' is not supported.")

    async def generate_response(self, prompt: str) -> str:
        try:
            model = genai.GenerativeModel(model_name=self.model)
            response = await asyncio.to_thread(model.generate_content, prompt)

            print("📤 Gemini raw response:", response)

            if hasattr(response, "text") and response.text:
                return response.text.strip()
            else:
                return "(No response received from Gemini)"

        except Exception as e:
            print("❌ Gemini API error:", e)
            return f"(API error: {e})"
