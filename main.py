import os import logging import asyncio import threading from flask import Flask from telegram import Update from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes import openai

=== Load env vars ===

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN") OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY") PORT = int(os.environ.get("PORT", 10000))

=== Logging ===

logging.basicConfig(level=logging.INFO) logger = logging.getLogger(name)

=== Flask keep-alive ===

flask_app = Flask(name)

@flask_app.route("/", methods=["GET"]) def home(): return "✅ MansourAI bot is running!"

=== Telegram handlers ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("Hello! I'm MansourAI 🤖 Ask me anything!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE): user_input = update.message.text try: response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[ {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": user_input} ] ) reply = response.choices[0].message.content except Exception as e: reply = f"⚠️ Error: {e}"

await update.message.reply_text(reply)

=== Telegram bot setup ===

def create_app(): app = ApplicationBuilder().token(BOT_TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(CommandHandler("ask", chat)) return app

=== Main entrypoint ===

if name == "main": openai.api_key = OPENAI_API_KEY

threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=PORT)).start()

import nest_asyncio
nest_asyncio.apply()

app = create_app()
logger.info("🤖 Starting MansourAI bot with polling...")
asyncio.get_event_loop().run_until_complete(app.run_polling())

