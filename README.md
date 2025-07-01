# 🤖 JARVIS Telegram AI Bot

A powerful Telegram bot that integrates with Google Gemini to act like a personal AI software engineer. Inspired by Jarvis from Iron Man.

---

## 🚀 Features

- 🔐 Developer-only mode or public mode toggle
- 🧠 AI (Gemini) powered bot building and code generation
- 📂 Can create, modify, and delete project files internally
- 📝 Upload `.txt` project plans for automatic AI buildout
- 🛠️ Auto-attempt error resolution and AI-generated explanations
- 🧼 File access restricted to safe folders (`bots/`, `shared/`, `config/`)

---

## 📁 Project Structure

```
jarvis_bot/
├── bots/                 # AI-generated bots
├── shared/               # Shared code written by AI
├── uploads/              # Uploaded plan files
├── config/
│   ├── settings.json     # Access mode and dev IDs
│   └── settings.py       # JSON read/write helpers
├── main.py               # Telegram bot logic
├── jarvis_engine.py      # Gemini prompt + logic
├── file_manager.py       # Filesystem handler
├── error_handler.py      # Explains AI errors simply
├── requirements.txt
├── Dockerfile
└── .env
```

---

## 🔧 Setup

### 1. Environment Variables

Create `.env` file:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_google_gemini_api_key
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Locally

```bash
python main.py
```

---

## 🐳 Docker

```bash
docker build -t jarvis-bot .
docker run --env-file .env jarvis-bot
```

---

## 🔑 Developer Access Mode

Modify `config/settings.json`:

```json
{
  "access_mode": "dev",
  "allowed_devs": [123456789]
}
```

Use `/access public` or `/access dev` in Telegram to toggle.

---

## ✉️ Commands

- `/jarvis [task]` – Give instructions to build/modify
- `/access [public|dev]` – Change access mode
- Upload `.txt` file – JARVIS reads and builds it

---

## 📜 License

MIT – Use freely, credit appreciated.

---

## 🧠 Powered by

- **Gemini Pro API**
- **Python 3.11**
- **Aiogram**