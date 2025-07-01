import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Debug log to verify env
print("🔍 ENV DEBUG")
print("TOKEN:", "✔️" if TOKEN else "❌")
print("OPENAI_KEY:", "✔️" if OPENAI_KEY else "❌")
print("WEBHOOK_URL:", "✔️" if WEBHOOK_URL else "❌")

# Validate
if not WEBHOOK_URL:
    raise ValueError("❌ WEBHOOK_URL is not set.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# Telegram app
bot = Bot(token=TOKEN)
telegram_app = Application.builder().token(TOKEN).build()

# Handlers
async def start(update: Update, context: ContextTypes
