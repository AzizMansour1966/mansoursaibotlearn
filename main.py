import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import openai

# === Configuration ===
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7788071056:AAECYEfIuxQYcCyS_DgAYaif1JHc_v9A5U8")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://mansoursaibotlearn.onrender.com/webhook")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "sk-...")  # replace with real key

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === OpenAI Setup ===
openai.api_key = OPENAI_API_KEY

# === Flask App ===
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ MansourAI bot is live (Webhook mode)"

@app.route("/webhook", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.process_update(update)
    return "OK"

# === Telegram Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm MansourAI 🤖 Ask me anything!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.effective_chat.id

    try:
        reply = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = reply['choices'][0]['message']['content']
    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"

    await context.bot.send_message(chat_id=chat_id, text=bot_reply)

# === Setup Application ===
bot = Bot(token=BOT_TOKEN)
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# === Set Webhook and Run Flask ===
if __name__ == "__main__":
    import nest_asyncio
    import asyncio

    nest_asyncio.apply()

    async def setup():
        await bot.set_webhook(WEBHOOK_URL)
        logger.info(f"🌐 Webhook set to {WEBHOOK_URL}")

    asyncio.get_event_loop().run_until_complete(setup())
    app.run(host="0.0.0.0", port=10000)
