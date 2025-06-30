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

# === Flask keep-alive ===
flask_app = Flask(__name__)

@flask_app.route("/", methods=["GET"])
def home():
    return "✅ MansourAI bot is running!"

# === Telegram command handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive and ready! 🚀")

# === Create and return bot application ===
def create_app():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    return app

# === Async bot runner ===
async def run_bot():
    app = create_app()
    logger.info("🤖 Starting MansourAI bot with polling...")
    await app.run_polling()

# === Main entrypoint ===
if __name__ == "__main__":
    # Start Flask server in a separate thread
    threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=PORT)).start()

    # Apply fix for "event loop is already running"
    import nest_asyncio
    nest_asyncio.apply()

    asyncio.get_event_loop().run_until_complete(run_bot())
