import os
from flask import Flask, request, abort
import telebot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError("Please set the TELEGRAM_TOKEN environment variable")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route("/")
def index():
    return "OK", 200

# Telegram will POST updates to https://<your-domain>/<TOKEN>
@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

# Simple echo handler
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Optional: if you set WEBHOOK_URL env var, set webhook automatically on start
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # e.g. "https://my-app.up.railway.app"
if WEBHOOK_URL:
    webhook = f"{WEBHOOK_URL.rstrip('/')}/{TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=webhook)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
