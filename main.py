import os
import logging
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Load environment variables ===
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7788071056:AAECYEfIuxQYcCyS_DgAYaif1JHc_v9A5U8")
PORT = int(os.environ.get("PORT", 10000))

# === Logging setup ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Flask keep-alive server ===
flask_app = Flask(__name__)

@flask_app.route("/", methods=["GET"])
def home():
    return "✅ MansourAI bot is running!"

# === Telegram command handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive and ready! 🚀")

# === Create the Telegram bot application ===
def create_bot_app():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    return app

# === Run the bot ===
async def run_bot():
    app = create_bot_app()
    logger.info("🤖 Starting MansourAI bot with polling...")
    await app.run_polling()

# === Main entry point ===
if __name__ == "__main__":
    # Start Flask in a background thread
    threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=PORT)).start()

    # Apply asyncio patch
    import nest_asyncio
    nest_asyncio.apply()

    # Start bot
    asyncio.run(run_bot())
