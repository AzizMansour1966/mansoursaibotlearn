import os
import logging
import asyncio
import threading
import openai

from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# === Environment Variables ===
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "your-fallback-token-here")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-fallback-openai-key")
PORT = int(os.environ.get("PORT", 10000))

# === Configure OpenAI ===
openai.api_key = OPENAI_API_KEY

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Flask App for Keep-Alive ===
flask_app = Flask(__name__)

@flask_app.route("/", methods=["GET"])
def home():
    return "✅ MansourAI bot is running!"

# === Telegram Command Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive and ready! 🚀")

async def chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("Please provide a prompt after /ask.")
        return

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        logger.exception("OpenAI API error")
        await update.message.reply_text("Something went wrong with OpenAI.")

# === Create Telegram App ===
def create_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", chatgpt))
    return app

# === Main Entrypoint ===
if __name__ == "__main__":
    # Start Flask server in background
    threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=PORT)).start()

    # Apply workaround for running in existing event loops
    import nest_asyncio
    nest_asyncio.apply()

    # Start Telegram bot
    bot_app = create_bot()
    logger.info("🤖 Starting MansourAI bot with polling...")
    asyncio.get_event_loop().run_until_complete(bot_app.run_polling())
