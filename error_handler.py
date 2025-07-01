# JARVIS Telegram Bot: error_handler.py

import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY

ERROR_PROMPT_PREFIX = """
You are an AI assistant. Your job is to explain programming errors in simple, beginner-friendly terms.

Explain the following error message:
"""

def handle_ai_error(error_msg: str) -> str:
    prompt = ERROR_PROMPT_PREFIX + error_msg
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(GEMINI_API_URL, json=payload)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return "An unexpected error occurred, and it couldn't be explained."