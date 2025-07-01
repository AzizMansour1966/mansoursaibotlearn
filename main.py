import os
from flask import Flask
from dotenv import load_dotenv

# ✅ Force load `.env.production` always (Render doesn't auto-load it)
load_dotenv(".env.production")

# 🔐 Now load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ❗ Raise errors if any are missing
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN is not set.")
if not WEBHOOK_URL:
    raise ValueError("❌ WEBHOOK_URL is not set.")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY is not set.")

# ✅ Initialize app
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is online!"

if __name__ == "__main__":
    app.run(debug=False, port=5000)
