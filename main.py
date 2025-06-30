import os import logging from flask import Flask, request from telegram import Update, Bot from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Dispatcher

=== Environment Variables ===

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7788071056:AAECYEfIuxQYcCyS_DgAYaif1JHc_v9A5U8") WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://mansoursaibotlearn.onrender.com") PORT = int(os.getenv("PORT", 10000))

=== Logging ===

logging.basicConfig(level=logging.INFO) logger = logging.getLogger(name)

=== Flask app ===

flask_app = Flask(name)

@flask_app.route("/", methods=["GET"]) def home(): return "✅ MansourAI bot is live via webhook!"

@flask_app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"]) def telegram_webhook(): update = Update.de_json(request.get_json(force=True), bot) application.update_queue.put_nowait(update) return "", 200

=== Telegram command handlers ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("Hello! I'm alive and ready! 🚀")

=== Telegram bot setup ===

bot = Bot(BOT_TOKEN) application = ApplicationBuilder().token(BOT_TOKEN).build() application.add_handler(CommandHandler("start", start))

if name == "main": # Set webhook logger.info("🔗 Setting webhook...") bot.delete_webhook() bot.set_webhook(url=f"{WEBHOOK_URL}/webhook/{BOT_TOKEN}")

# Start Flask server
logger.info(f"🚀 Starting MansourAI bot on port {PORT} with webhook...")
flask_app.run(host="0.0.0.0", port=PORT)

