import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ContextTypes, filters
)
from dotenv import load_dotenv
import requests
import nest_asyncio  # ✅ FIX
nest_asyncio.apply()  # ✅ Needed for async inside sync (Flask)

# Load .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# Telegram app
application = Application.builder().token(TOKEN).build()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm alive and ready!")

application.add_handler(CommandHandler("start", start))

# Shared event loop (to avoid asyncio.run)
loop = asyncio.get_event_loop()

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        json_data = request.get_json(force=True)
        update = Update.de_json(json_data, application.bot)

        async def process():
            await application.initialize()
            await application.process_update(update)

        # ✅ Run in same loop (no block or pool error)
        loop.create_task(process())
        return "OK", 200
    except Exception as e:
        logger.exception("❌ Error processing update")
        return "Webhook error", 500

# Start
if __name__ == "__main__":
    logger.info("🚀 Starting bot server...")
    logger.info(f"TOKEN: {'✔️' if TOKEN else '❌'}")
    logger.info(f"WEBHOOK_URL: {'✔️' if WEBHOOK_URL else '❌'}")

    # Set webhook
    response = requests.get(
        f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}/webhook"
    )
    logger.info("📡 Webhook response: %s", response.json())

    app.run(host="0.0.0.0", port=5000)
