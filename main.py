import os
from flask import Flask
from dotenv import load_dotenv

# ✅ Get path to .env.production relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env.production")

# 🔁 Load .env.production even on Render
load_dotenv(ENV_PATH)

# ✅ Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ❌ Crash if anything is missing
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN is not set.")
if not WEBHOOK_URL:
    raise ValueError("❌ WEBHOOK_URL is not set.")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY is not set.")

# ✅ Flask app starts here
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(debug=False, port=5000)
