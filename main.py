main.py

import os import logging from flask import Flask from telegram import Update from telegram.ext import ( ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters ) import openai import nest_asyncio import threading import asyncio

=== Configuration ===

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE") OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE") PORT = int(os.environ.get("PORT", 10000)) openai.api_key = OPENAI_API_KEY

=== Logging ===

logging.basicConfig(level=logging.INFO) logger = logging.getLogger(name)

=== Flask Keep-Alive ===

flask_app = Flask(name)

@flask_app.route("/") def home(): return "✅ MansourAI bot is running!"

=== Handlers ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("Hello! I'm alive and ready! 🚀")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): user_message = update.message.text logger.info(f"Received message: {user_message}")

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly and funny assistant."},
            {"role": "user", "content": user_message}
        ]
    )
    reply = response.choices[0].message.content
except Exception as e:
    logger.error(f"OpenAI error: {e}")
    reply = "Oops! Something went wrong with the AI."

await update.message.reply_text(reply)

=== Bot Setup ===

def create_bot(): app = ApplicationBuilder().token(BOT_TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) return app

=== Run ===

if name == "main": nest_asyncio.apply() threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=PORT)).start()

bot_app = create_bot()
asyncio.run(bot_app.run_polling())

