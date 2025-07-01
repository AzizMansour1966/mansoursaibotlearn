import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes
)
from dotenv import load_dotenv
import requests

# Load environment variables from .env.production explicitly
load_dotenv(dotenv_path=".env.production")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Telegram Application (async)
application = Application.builder().token(TOKEN).build()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /start command from user %s", update.effective_user.id)
    await update.message.reply_text("👋 Hello! I'm alive and ready!")

application.add_handler(CommandHandler("start", start))

# Flask webhook route (sync) for Render compatibility
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        json_data = request.get_json(force=True)
        update = Update.de_json(json_data, application.bot)

        async def process_update():
            await application.initialize()
            await application.process_update(update)

        asyncio.run(process_update())
        return "OK", 200
    except Exception as e:
        logger.exception("❌ Error in webhook processing: %s", e)
        return "Webhook error", 500

if __name__ == "__main__":
    logger.info("🚀 Starting bot server...")
    logger.info(f"TOKEN: {'✔️' if TOKEN else '❌'}")
    logger.info(f"OPENAI_KEY: {'✔️' if OPENAI_KEY else '❌'}")
    logger.info(f"WEBHOOK_URL: {'✔️' if WEBHOOK_URL else '❌'}")

    # Set webhook on Telegram side
    try:
        set_webhook_resp = requests.get(
            f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}/webhook"
        )
        logger.info("📡 Telegram setWebhook response: %s", set_webhook_resp.json())
    except Exception as e:
        logger.error("Failed to set Telegram webhook: %s", e)

    # Run Flask app
    app.run(host="0.0.0.0", port=5000)
