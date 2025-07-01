import os
from flask import Flask, request
from dotenv import load_dotenv

# 🔁 Automatically load `.env.production` if on Render (production)
env_file = ".env.production" if os.getenv("RENDER") else ".env"
load_dotenv(env_file)

# ✅ Now these will work:
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ❌ Error if critical vars are missing
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN is not set.")
if not WEBHOOK_URL:
    raise ValueError("❌ WEBHOOK_URL is not set.")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY is not set.")

# ✅ Example bot app (simplified)
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is alive!"

if __name__ == "__main__":
    app.run(debug=False, port=5000)
