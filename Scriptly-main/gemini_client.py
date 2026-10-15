"""
gemini_client.py
-----------------
Thin wrapper around the Google Gemini API so every agent talks to the
model the same way (same config, same error handling).
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Create a .env file (copy .env.example) "
        "and paste your Gemini API key into it. Locally, or set it as an "
        "environment variable in your hosting dashboard if deployed."
    )

genai.configure(api_key=API_KEY)


def call_gemini(system_instruction: str, user_prompt: str, temperature: float = 0.7) -> str:
    """
    Sends a prompt to Gemini and returns the plain text response.
    Each agent passes its own `system_instruction` so the model plays
    the right "role" (researcher, writer, editor).
    """
    try:
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            system_instruction=system_instruction,
        )
        response = model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(temperature=temperature),
        )
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Gemini API call failed: {str(e)}")
