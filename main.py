import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes, MessageHandler, filters
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env.production")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# Telegram application (lazy, async-compatible)
application = Application.builder().token(TOKEN).build()

# --- Telegram Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm alive and ready!")

# Register handlers
application.add_handler(CommandHandler("start", start))

# --- Webhook route (Sync wrapper for async calls) ---
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)

        async def process():
            await application.initialize()
            await application.process_update(update)

        asyncio.run(process())
        return "OK", 200
    except Exception as e:
        logger.exception("❌ Webhook error")
        return "Webhook error", 500

# --- App Startup ---
if __name__ == "__main__":
    logger.info("🚀 Starting bot server...")
    logger.info(f"TOKEN: {'✔️' if TOKEN else '❌'}")
    logger.info(f"OPENAI_KEY: {'✔️' if OPENAI_KEY else '❌'}")
    logger.info(f"WEBHOOK_URL: {'✔️' if WEBHOOK_URL else '❌'}")

    # Set webhook at startup
    import requests
    res = requests.get(
        f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}/webhook"
    )
    logger.info("📡 Webhook response: %s", res.json())

    # Start Flask
    app.run(host="0.0.0.0", port=5000)
