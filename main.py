import os import logging from flask import Flask, request from telegram import Update from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes import openai

=== Load env vars ===

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7788071056:AAECYEfIuxQYcCyS_DgAYaif1JHc_v9A5U8") WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://mansoursaibotlearn.onrender.com") PORT = int(os.environ.get("PORT", 10000))

=== Logging ===

logging.basicConfig(level=logging.INFO) logger = logging.getLogger(name)

=== Flask keep-alive and webhook handler ===

flask_app = Flask(name)

@flask_app.route("/") def index(): return "✅ MansourAI Bot is alive and running."

@flask_app.post("/webhook") async def webhook(): if request.method == "POST": await application.update_queue.put(Update.de_json(request.get_json(force=True), application.bot)) return "", 200

=== Telegram handlers ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("Hello! I'm alive and ready! 🚀")

=== Telegram bot setup ===

application = ApplicationBuilder().token(BOT_TOKEN).build() application.add_handler(CommandHandler("start", start))

=== Webhook startup ===

async def run(): logger.info("📡 Setting webhook...") await application.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook") await application.initialize() await application.start()

if name == "main": import asyncio import nest_asyncio nest_asyncio.apply()

import threading
threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=PORT)).start()

asyncio.get_event_loop().run_until_complete(run())

