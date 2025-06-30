import os
import logging
import asyncio
import threading
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import httpx
import openai
import nest_asyncio

# === Load tokens ===
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7788071056:AAECYEfIuxQYcCyS_DgAYaif1JHc_v9A5U8")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "sk-your-real-openai-key-here")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://mansoursaibotlearn.onrender.com/webhook")

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Flask app ===
flask_app = Flask(__name__)

@flask_app.route("/", methods=["GET"])
def home():
    return "✅ MansourAI bot is live with webhook!"

@flask_app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json()
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return "OK"

# === GPT-3.5 handler ===
async def ask_gpt(prompt):
    openai.api_key = OPENAI_API_KEY
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# === Telegram handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Send me a message and I’ll ask ChatGPT!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    reply = await ask_gpt(user_msg)
    await update.message.reply_text(reply)

# === Setup bot ===
bot = Bot(token=BOT_TOKEN)
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# === Entrypoint ===
if __name__ == "__main__":
    nest_asyncio.apply()

    # Set webhook
    async def set_webhook():
        await bot.set_webhook(url=WEBHOOK_URL)
        logger.info(f"🌐 Webhook set to {WEBHOOK_URL}")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_webhook())

    # Run Flask server
    threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=10000)).start()
