import os
import logging
from flask import Flask, request
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# ✅ Load environment variables (Render injects these; no .env.production needed)
load_dotenv()

# ✅ Get env vars injected by Render
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# ❌ If missing, fail early
if not WEBHOOK_URL:
    raise ValueError("❌ WEBHOOK_URL is not set.")

# ✅ Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Flask app setup
app = Flask(__name__)
bot = Bot(token=TOKEN)

# ✅ Telegram application setup
telegram_app = Application.builder().token(TOKEN).build()

# ✅ Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm alive and ready.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# ✅ Flask routes
@app.route("/", methods=["GET"])
def healthcheck():
    return "✅ Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK"

# ✅ Set Telegram webhook
@app.before_first_request
def setup_webhook():
    webhook_set = bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    if webhook_set:
        logger.info("✅ Webhook set successfully.")
    else:
        logger.error("❌ Failed to set webhook.")

# ✅ Start Flask app
if __name__ == "__main__":
    logger.info("🚀 Starting bot server...")
    app.run(host="0.0.0.0", port=5000)
