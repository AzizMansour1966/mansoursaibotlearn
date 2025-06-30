import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# Load your secrets from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Flask setup
app = Flask(__name__)

# Telegram Bot and Application
bot = Bot(token=BOT_TOKEN)
application = Application.builder().token(BOT_TOKEN).build()

# === Your Telegram handlers ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive.")

application.add_handler(CommandHandler("start", start))

# === Webhook route ===

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)
        asyncio.create_task(application.process_update(update))
        return "OK", 200
    except Exception as e:
        print(f"Webhook error: {e}")
        return "Error", 500

# === Health check route ===

@app.route("/", methods=["GET"])
def index():
    return "Bot is alive", 200

# === App startup ===

if __name__ == "__main__":
    # Set the webhook on startup
    async def set_webhook():
        await bot.set_webhook(WEBHOOK_URL)
        print(f"🌐 Webhook set to {WEBHOOK_URL}")

    asyncio.run(set_webhook())

    # Run Flask server
    app.run(host="0.0.0.0", port=10000)
