import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load environment from .env
load_dotenv()

# Get vars
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Safety checks
if not BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN not set.")
if not WEBHOOK_URL:
    raise ValueError("❌ WEBHOOK_URL not set.")

# Flask App
app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
application = Application.builder().token(BOT_TOKEN).build()

# Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is live!")

application.add_handler(CommandHandler("start", start))

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        asyncio.create_task(application.process_update(update))
        return "OK", 200
    except Exception as e:
        print(f"Webhook error: {e}")
        return "Error", 500

# Health check
@app.route("/", methods=["GET"])
def health():
    return "🤖 Bot running", 200

# Start server
if __name__ == "__main__":
    async def setup():
        await bot.set_webhook(WEBHOOK_URL)
        print(f"🌐 Webhook set: {WEBHOOK_URL}")

    asyncio.run(setup())
    app.run(host="0.0.0.0", port=10000)
