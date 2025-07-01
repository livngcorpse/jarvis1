# JARVIS Telegram Bot: file_manager.py

import os
import pathlib

BASE_DIR = os.path.abspath(".")
ALLOWED_ROOTS = ["bots", "shared", "config"]

def apply_ai_response(ai_response: dict):
    files = ai_response.get("files", {})
    if not files:
        raise Exception("No files found in AI response.")

    for path, content in files.items():
        safe_path = sanitize_path(path)
        full_path = os.path.join(BASE_DIR, safe_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

def sanitize_path(path: str) -> str:
    normalized = pathlib.Path(path).as_posix()
    root_folder = normalized.split("/")[0]
    if root_folder not in ALLOWED_ROOTS:
        raise Exception(f"Path '{path}' is outside allowed directories.")
    return normalized
