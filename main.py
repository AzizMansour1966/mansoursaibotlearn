import os
import logging
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Load env vars ===
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7788071056:AAECYEfIuxQYcCyS_DgAYaif1JHc_v9A5U8")
PORT = int(os.environ.get("PORT", 10000))

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Flask keep-alive ===
flask_app = Flask(__name__)

@flask_app.route("/", methods=["GET"])
def home():
    return "✅ MansourAI bot is running!"

# === Telegram handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive and ready! 🚀")

# === Telegram bot setup ===
def create_bot_app():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    return app

# === Main entrypoint ===
async def run_bot():
    app = create_bot_app()
    logger.info("🤖 Starting MansourAI bot with polling...")
    await app.run_polling()

if __name__ == "__main__":
    # Start Flask server in background
    threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=PORT)).start()

    # Run the bot
    asyncio.run(run_bot())
