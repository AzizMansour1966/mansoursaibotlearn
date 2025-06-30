import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === Load tokens from environment ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# === Safety check ===
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN is missing. Set it in the environment variables.")
if not WEBHOOK_URL:
    raise ValueError("❌ WEBHOOK_URL is missing. Set it in the environment variables.")

# === Flask App ===
app = Flask(__name__)

# === Telegram Bot and Application ===
bot = Bot(token=BOT_TOKEN)
application = Application.builder().token(BOT_TOKEN).build()

# === Telegram Command Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running!")

application.add_handler(CommandHandler("start", start))

# === Webhook endpoint ===
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)
        asyncio.create_task(application.process_update(update))
        return "OK", 200
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return "Error", 500

# === Health Check ===
@app.route("/", methods=["GET"])
def index():
    return "🤖 Bot is alive", 200

# === Startup ===
if __name__ == "__main__":
    async def setup():
        await bot.set_webhook(WEBHOOK_URL)
        print(f"🌐 Webhook set to {WEBHOOK_URL}")

    asyncio.run(setup())
    app.run(host="0.0.0.0", port=10000)
