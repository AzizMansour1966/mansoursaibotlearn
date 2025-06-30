import os import logging import asyncio from flask import Flask, request from telegram import Update, Bot from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes import openai import nest_asyncio

=== Environment Variables and Tokens ===

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7788071056:AAECYEfIuxQYcCyS_DgAYaif1JHc_v9A5U8") OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "sk-skipped-for-safety") WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://mansoursaibotlearn.onrender.com/webhook") PORT = int(os.environ.get("PORT", 10000))

=== Configure OpenAI ===

openai.api_key = OPENAI_API_KEY

=== Logging ===

logging.basicConfig(level=logging.INFO) logger = logging.getLogger(name)

=== Flask App ===

flask_app = Flask(name)

@flask_app.route("/") def index(): return "✅ MansourAI bot is running via webhook!"

@flask_app.route("/webhook", methods=["POST"]) def webhook(): if request.method == "POST": update = Update.de_json(request.get_json(force=True), bot) asyncio.run(application.process_update(update)) return "!"

=== Telegram Handlers ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("Hello! I'm alive and ready! 🚀")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE): question = update.message.text.replace("/ask", "").strip() if not question: await update.message.reply_text("Please ask a question after /ask") return

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": question}],
)
answer = response.choices[0].message.content
await update.message.reply_text(answer)

=== App Initialization ===

bot = Bot(BOT_TOKEN) application = ApplicationBuilder().token(BOT_TOKEN).build() application.add_handler(CommandHandler("start", start)) application.add_handler(CommandHandler("ask", ask))

=== Set Webhook and Run ===

if name == "main": nest_asyncio.apply()

# Set the webhook only once
bot.delete_webhook()
bot.set_webhook(url=WEBHOOK_URL)
logger.info(f"🌐 Webhook set to {WEBHOOK_URL}")

# Start Flask
flask_app.run(host="0.0.0.0", port=PORT)

