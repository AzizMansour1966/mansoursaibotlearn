import os import logging import asyncio import threading from flask import Flask, request from telegram import Update, Bot from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes import openai import nest_asyncio

=== Config ===

BOT_TOKEN = "7788071056:AAECYEfIuxQYcCyS_DgAYaif1JHc_v9A5U8" WEBHOOK_URL = "https://mansoursaibotlearn.onrender.com" PORT = int(os.environ.get("PORT", 10000))

=== Logging ===

logging.basicConfig(level=logging.INFO) logger = logging.getLogger(name)

=== Flask Keep-Alive ===

flask_app = Flask(name)

@flask_app.route("/", methods=["GET"]) def home(): return "✅ MansourAI bot is running with webhook!"

@flask_app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"]) def webhook(): update = Update.de_json(request.get_json(force=True), bot) asyncio.run(app.process_update(update)) return "", 200

=== Telegram Handlers ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("Hello! I'm alive and ready to chat with GPT-3.5! 🚀")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): user_input = update.message.text try: response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[ {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": user_input}, ] ) reply_text = response.choices[0].message.content await update.message.reply_text(reply_text) except Exception as e: await update.message.reply_text("⚠️ Sorry, something went wrong.") logger.error(f"OpenAI error: {e}")

=== Telegram App Setup ===

app = ApplicationBuilder().token(BOT_TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(CommandHandler("help", start)) app.add_handler(CommandHandler("chat", handle_message)) app.add_handler(CommandHandler("ask", handle_message)) app.add_handler(CommandHandler(None, handle_message))

bot = Bot(BOT_TOKEN)

=== Main Entrypoint ===

if name == "main": nest_asyncio.apply() bot.delete_webhook() bot.set_webhook(url=f"{WEBHOOK_URL}/webhook/{BOT_TOKEN}") logger.info("📡 Webhook set. Starting Flask server...") flask_app.run(host="0.0.0.0", port=PORT)

