import os
import logging
import asyncio
import nest_asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Allow nested event loops in Flask environment
nest_asyncio.apply()

# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram Application once
application = Application.builder().token(TOKEN).build()

# Define start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received /start from user {update.effective_user.id}")
    await update.message.reply_text("👋 Hello! I'm alive and ready!")

# Register command handler
application.add_handler(CommandHandler("start", start))

# Webhook route (async friendly)
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        json_data = request.get_json(force=True)
        update = Update.de_json(json_data, application.bot)
        logger.info("Webhook update received")

        # Run update processing asynchronously without creating new loop
        loop = asyncio.get_event_loop()
        loop.create_task(application.process_update(update))

        return "OK", 200
    except Exception as e:
        logger.exception("❌ Error processing webhook update")
        return "Webhook error", 500

# Main entry point
if __name__ == "__main__":
    logger.info("🚀 Starting bot server...")
    logger.info(f"TOKEN: {'✔️' if TOKEN else '❌'}")
    logger.info(f"OPENAI_KEY: {'✔️' if OPENAI_KEY else '❌'}")
    logger.info(f"WEBHOOK_URL: {'✔️' if WEBHOOK_URL else '❌'}")

    # Set webhook URL
    import requests
    response = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}/webhook")
    logger.info("📡 Webhook set response: %s", response.json())

    # Start Flask server
    app.run(host="0.0.0.0", port=5000)
