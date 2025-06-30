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

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Flask keep-alive app ===
flask_app = Flask(__name__)

@flask_app.route("/", methods=["GET"])
def home():
    return "✅ MansourAI bot is running!"

# === Telegram command handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive and ready! 🚀")

# === Create bot application ===
def create_bot_app():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    return app

# Create the app once (to avoid duplicate handler registration)
app = create_bot_app()

# === Async bot runner ===
async def run_bot():
    logger.info("🤖 Starting MansourAI bot with polling...")
    await app.run_polling()

# === Main entrypoint ===
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()

    # Start Flask keep-alive server in a background thread
    threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=PORT)).start()

    # Start the bot using asyncio
    asyncio.run(run_bot())
