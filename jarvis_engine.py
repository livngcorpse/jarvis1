# JARVIS Telegram Bot: jarvis_engine.py

import os
import requests
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY
print("🔑 GEMINI KEY:", GEMINI_API_KEY)

INSTRUCTION_PROMPT = """
You are JARVIS — an expert AI software engineer.
Respond ONLY in this JSON format:
{
  "files": {
    "path/to/file.py": "<python or content>"
  }
}
Do NOT include commentary or explanation. Follow request as strictly as possible.
"""

def process_prompt(user_prompt: str) -> dict:
    full_prompt = INSTRUCTION_PROMPT + "\n" + user_prompt
    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}]
    }

    response = requests.post(GEMINI_API_URL, json=payload)
    response.raise_for_status()
    content = response.json()["candidates"][0]["content"]["parts"][0]["text"]

    return parse_response_json(content)

def parse_response_json(raw_text: str) -> dict:
    import json
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        raise Exception("Invalid JSON received from Gemini.\n\nResponse:\n" + raw_text)
