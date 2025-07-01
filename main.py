import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# === Load local .env file (for dev) ===
load_dotenv()

# === Load environment variables ===
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# === Debug logging ===
print("🔍 TELEGRAM_BOT_TOKEN =", BOT_TOKEN)
print("🔍 WEBHOOK_URL =", repr(WEBHOOK_URL))  # Use repr to catch hidden newlines/spaces

# === Error handling ===
if not BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN is not set.")
if not WEBHOOK_URL:
    raise ValueError("❌ WEBHOOK_URL is not set.")

# === Flask setup ===
app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
application = Application.builder().token(BOT_TOKEN).build()

# === Telegram command handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running!")

application.add_handler(CommandHandler("start", start))

# === Webhook endpoint ===
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            print("⚠️ Loop is closed. Skipping webhook processing.")
            return "Shutting down", 503
        asyncio.create_task(application.process_update(update))
        return "OK", 200
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return "Error", 500

# === Health check ===
@app.route("/", methods=["GET"])
def index():
    return "🤖 Bot is alive", 200

# === Start bot with webhook ===
if __name__ == "__main__":
    async def setup():
        await bot.set_webhook(WEBHOOK_URL)
        print(f"🌐 Webhook set to: {WEBHOOK_URL}")

    asyncio.run(setup())
    app.run(host="0.0.0.0", port=10000)
