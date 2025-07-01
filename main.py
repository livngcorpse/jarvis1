import json
import logging
from aiogram import Bot, Dispatcher, executor, types
from jarvis_engine import process_prompt
from file_manager import apply_ai_response
from error_handler import handle_ai_error
from config.settings import get_settings, save_settings
import os
from dotenv import load_dotenv
load_dotenv()


API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

settings = get_settings()

# Helper to check if user is allowed to use JARVIS
def is_user_allowed(user_id: int) -> bool:
    if settings["access_mode"] == "everyone":
        return True
    return user_id in settings["allowed_devs"]

@dp.message_handler(commands=['jarvis'])
async def handle_jarvis_command(message: types.Message):
    if not is_user_allowed(message.from_user.id):
        await message.reply("❌ You don't have permission to use JARVIS.")
        return

    prompt = message.get_args()
    if not prompt:
        await message.reply("⚠️ Please provide a command or task.")
        return

    for attempt in range(1, 6):
        try:
            ai_response = process_prompt(prompt)
            apply_ai_response(ai_response)
            await message.reply(f"✅ Task completed successfully on attempt #{attempt}.")
            break
        except Exception as e:
            explanation = handle_ai_error(str(e))
            await message.reply(f"❌ Attempt #{attempt} failed.\nError: {explanation}")
            if attempt == 5:
                await message.reply("❌ All 5 attempts failed. Please check the plan or rephrase your request.")

@dp.message_handler(commands=['access'])
async def handle_access_mode(message: types.Message):
    if message.from_user.id not in settings["allowed_devs"]:
        await message.reply("⚠️ Only developers can change access modes.")
        return

    args = message.get_args().strip().lower()
    if args == "public":
        settings["access_mode"] = "everyone"
        save_settings(settings)
        await message.reply("✅ JARVIS is now available to everyone.")
    elif args == "dev":
        settings["access_mode"] = "dev"
        save_settings(settings)
        await message.reply("✅ JARVIS is now restricted to developers only.")
    else:
        await message.reply("❌ Invalid option. Use /access public or /access dev.")

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_file_upload(message: types.Message):
    if not is_user_allowed(message.from_user.id):
        await message.reply("❌ You don't have permission to use JARVIS.")
        return

    file = await message.document.download(destination_dir="uploads/")
    with open(file.name, "r") as f:
        plan = f.read()

    prompt = f"User uploaded plan:\n{plan}\n\nBuild the described system accordingly."
    for attempt in range(1, 6):
        try:
            ai_response = process_prompt(prompt)
            apply_ai_response(ai_response)
            await message.reply(f"✅ Project built successfully from uploaded file (Attempt #{attempt}).")
            break
        except Exception as e:
            explanation = handle_ai_error(str(e))
            await message.reply(f"❌ Attempt #{attempt} failed.\nError: {explanation}")
            if attempt == 5:
                await message.reply("❌ All 5 attempts failed. Please review the plan.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)