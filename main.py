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

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram Application
application = Application.builder().token(TOKEN).build()

# Define handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm alive and ready!")

# Register handlers
application.add_handler(CommandHandler("start", start))

# Flask route for webhook
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
        logger.exception("❌ Error processing update")
        return "Webhook error", 500

# Main app entry point
if __name__ == "__main__":
    logger.info("🚀 Starting bot server...")
    logger.info(f"TOKEN: {'✔️' if TOKEN else '❌'}")
    logger.info(f"OPENAI_KEY: {'✔️' if OPENAI_KEY else '❌'}")
    logger.info(f"WEBHOOK_URL: {'✔️' if WEBHOOK_URL else '❌'}")

    # Set Telegram webhook (run once per deploy)
    response = requests.get(
        f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}/webhook"
    )
    logger.info("📡 Webhook response: %s", response.json())

    # Run Flask server
    app.run(host="0.0.0.0", port=5000)
