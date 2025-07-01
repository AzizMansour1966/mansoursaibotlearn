import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

# Load environment variables
load_dotenv()  # ✅ works both locally and in Render if variables are defined

# Fetch required tokens
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Debug: Show what's loaded
print("🔍 ENV DEBUG")
print("TOKEN:", "✔️" if TOKEN else "❌")
print("OPENAI_KEY:", "✔️" if OPENAI_KEY else "❌")
print("WEBHOOK_URL:", "✔️" if WEBHOOK_URL else "❌")

# Check essential variable
if not WEBHOOK_URL:
    raise ValueError("❌ WEBHOOK_URL is not set.")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask setup
app = Flask(__name__)
bot = Bot(token=TOKEN)

# Telegram application
telegram_app = Application.builder().token(TOKEN).build()

# Telegram command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm alive and ready.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Health check endpoint
@app.route("/", methods=["GET"])
def healthcheck():
    return "✅ Bot is running!"

# Webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK"

# Manual setup endpoint to register webhook (Flask 3 compatible)
@app.route("/setup", methods=["GET"])
def setup_webhook():
    success = bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    if success:
        logger.info("✅ Webhook set successfully.")
        return "✅ Webhook set successfully."
    else:
        logger.error("❌ Failed to set webhook.")
        return "❌ Failed to set webhook.", 500

# Run server
if __name__ == "__main__":
    logger.info("🚀 Starting bot server...")
    app.run(host="0.0.0.0", port=5000)
