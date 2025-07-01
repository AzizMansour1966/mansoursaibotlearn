import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes, MessageHandler, filters
)
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# Telegram app (deferred setup)
application = Application.builder().token(TOKEN).build()

# --- Command handler ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive and ready! 🚀")

application.add_handler(CommandHandler("start", start))

# --- Webhook route (sync-compatible for Flask) ---
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        asyncio.run(application.initialize())
        asyncio.run(application.process_update(update))
        return "OK", 200
    except Exception as e:
        logger.exception("❌ Webhook error")
        return "Webhook error", 500

# --- Startup ---
if __name__ == "__main__":
    logger.info("🚀 Starting bot server...")
    logger.info("🔍 ENV DEBUG")
    logger.info(f"TOKEN: {'✔️' if TOKEN else '❌'}")
    logger.info(f"OPENAI_KEY: {'✔️' if OPENAI_KEY else '❌'}")
    logger.info(f"WEBHOOK_URL: {'✔️' if WEBHOOK_URL else '❌'}")

    # Set webhook
    res = requests.get(
        f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}/webhook"
    )
    logger.info("📡 Webhook set response: %s", res.json())

    # Run Flask server
    app.run(host="0.0.0.0", port=5000)
