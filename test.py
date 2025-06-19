import google.generativeai as genai

# Paste your Gemini API key here
api_key = "AIzaSyAr9a0GFYXRPET-_erOTI4SzQE-0Sku7ys"

# Set the key
genai.configure(api_key=api_key)

# Try a simple call
try:
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content("Say hello")
    print("✅ Gemini is working!")
    print("Response:", response.text)
except Exception as e:
    print("❌ Gemini API test failed:")
    print(e)
