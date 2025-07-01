limport os
from dotenv import load_dotenv
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ✅ Only load .env.production if NOT on Render
if not os.getenv("RENDER"):
    load_dotenv(".env.production")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# ❌ Fail fast if not set
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN is not set.")
if not WEBHOOK_URL:
    raise ValueError("❌ WEBHOOK_URL is not set.")

# 📝 Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🧠 Flask + Telegram App
app = Flask(__name__)
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# ✅ Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your bot.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# 🌐 Webhook endpoint
@app.post("/webhook")
async def webhook():
    update = Update.de_json(request.json, telegram_app.bot)
    await telegram_app.process_update(update)
    return "OK"

# 🚀 Start bot with webhook
async def run():
    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(WEBHOOK_URL)
    await telegram_app.start()
    logger.info(f"🚀 Bot started with webhook {WEBHOOK_URL}")

import asyncio
if __name__ == "__main__":
    asyncio.run(run())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
