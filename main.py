import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import nest_asyncio
import asyncio

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

logger.info("🔍 ENV DEBUG")
logger.info(f"TOKEN: {'✔️' if TOKEN else '❌'}")
logger.info(f"OPENAI_KEY: {'✔️' if OPENAI_KEY else '❌'}")
logger.info(f"WEBHOOK_URL: {'✔️' if WEBHOOK_URL else '❌'}")

if not all([TOKEN, OPENAI_KEY, WEBHOOK_URL]):
    raise ValueError("❌ One or more required environment variables are missing.")

# Set up Flask
app = Flask(__name__)

# Enable nested event loops (important for Render)
nest_asyncio.apply()

# Create Telegram bot application
bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).build()

# Define command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive and ready! 🚀")

# Register handlers
application.add_handler(CommandHandler("start", start))

# Set webhook route
@app.route("/webhook", methods=["POST"])
async def webhook() -> str:
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        await application.process_update(update)
        return "OK"
    return "Method not allowed", 405

# Set the webhook before the first request
@app.before_request
def setup_webhook_once():
    if not application.bot_data.get("webhook_set"):
        asyncio.get_event_loop().create_task(application.bot.set_webhook(url=WEBHOOK_URL))
        application.bot_data["webhook_set"] = True
        logger.info("✅ Webhook set on bot startup.")

# Root route
@app.route("/", methods=["GET"])
def home():
    return "Webhook set successfully."

# Run the Flask app
if __name__ == "__main__":
    logger.info("🚀 Starting bot server...")
    app.run(host="0.0.0.0", port=5000)
