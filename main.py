import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

# Load .env if running locally (has no effect on Render unless file is included manually)
load_dotenv()

# Fetch environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# DEBUG: Log environment keys for Render verification
print("🔍 ENV DEBUG")
print("TOKEN:", "✔️" if TOKEN else "❌ MISSING")
print("OPENAI_KEY:", "✔️" if OPENAI_KEY else "❌ MISSING")
print("WEBHOOK_URL:", "✔️" if WEBHOOK_URL else "❌ MISSING")

if not WEBHOOK_URL:
    raise ValueError("❌ WEBHOOK_URL is not set.")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app setup
app = Flask(__name__)
bot = Bot(token=TOKEN)

# Telegram application setup
telegram_app = Application.builder().token(TOKEN).build()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm alive and ready.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Health check
@app.route("/", methods=["GET"])
def healthcheck():
    return "✅ Bot is running!"

# Telegram webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK"

# Set webhook on first request
@app.before_first_request
def setup_webhook():
    success = bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    if success:
        logger.info("✅ Webhook set successfully.")
    else:
        logger.error("❌ Failed to set webhook.")

# Run Flask app
if __name__ == "__main__":
    logger.info("🚀 Starting bot server...")
    app.run(host="0.0.0.0", port=5000)
