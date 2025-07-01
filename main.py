import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import asyncio

# Load env vars
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# Shared asyncio event loop
loop = asyncio.get_event_loop()

# Telegram bot app
application = Application.builder().token(TOKEN).build()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm alive and ready!")

application.add_handler(CommandHandler("start", start))

# Webhook route
@app.post("/webhook")
async def webhook():
    try:
        json_data = request.get_json(force=True)
        update = Update.de_json(json_data, application.bot)

        await application.initialize()
        await application.process_update(update)

        return "OK", 200
    except Exception as e:
        logger.exception("❌ Webhook processing failed")
        return "Webhook error", 500

# Optional: route for root status check
@app.get("/")
def index():
    return "🤖 MansoursAI is live!", 200

# Start app
if __name__ == "__main__":
    logger.info("🚀 Starting MansoursAI bot...")
    logger.info(f"TOKEN: {'✔️' if TOKEN else '❌'}")
    logger.info(f"OPENAI_KEY: {'✔️' if OPENAI_KEY else '❌'}")
    logger.info(f"WEBHOOK_URL: {'✔️' if WEBHOOK_URL else '❌'}")

    # Set webhook once
    import requests
    r = requests.get(
        f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}/webhook"
    )
    logger.info("📡 Webhook set result: %s", r.json())

    app.run(host="0.0.0.0", port=5000)
