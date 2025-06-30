import os import logging import openai from flask import Flask, request from telegram import Bot, Update from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

=== Constants ===

BOT_TOKEN = "7788071056:AAECYEfIuxQYcCyS_DgAYaif1JHc_v9A5U8" OPENAI_API_KEY = "sk-proj-4gALccr-Fg2MbJ_-iV511ZPmKgEwlI0v7pVAvbFjAZXGNgF" WEBHOOK_URL = "https://mansoursaibotlearn.onrender.com" PORT = int(os.environ.get("PORT", 10000))

=== Logging ===

logging.basicConfig(level=logging.INFO) logger = logging.getLogger(name)

=== OpenAI API ===

openai.api_key = OPENAI_API_KEY

def ask_gpt(message_text): try: response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[{"role": "user", "content": message_text}] ) return response.choices[0].message.content.strip() except Exception as e: logger.error(f"OpenAI error: {e}") return "Sorry, something went wrong."

=== Flask App ===

flask_app = Flask(name) bot = Bot(token=BOT_TOKEN)

@flask_app.route("/", methods=["GET"]) def index(): return "✅ MansourAI bot is running!"

@flask_app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"]) def webhook(): if request.method == "POST": update = Update.de_json(request.get_json(force=True), bot) app.update_queue.put(update) return "OK"

=== Handlers ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("Hello! I'm alive and ready! 🚀")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): user_message = update.message.text reply = ask_gpt(user_message) await update.message.reply_text(reply)

=== Telegram Application ===

app = ApplicationBuilder().token(BOT_TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if name == "main": # Set webhook webhook_url = f"{WEBHOOK_URL}/webhook/{BOT_TOKEN}" bot.set_webhook(url=webhook_url) logger.info(f"🚀 Webhook set to {webhook_url}")

# Start Flask app
flask_app.run(host="0.0.0.0", port=PORT)

