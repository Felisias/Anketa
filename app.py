import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get("TELEGRAM_TOKEN", "8206831751:AAEl6mop8BF0wQFJydf0wiOFtmq1Nz0H2kk")
WEBHOOK_HOST = "https://твой-домен.onrender.com"  # замени на свой Render-домен
WEBHOOK_URL = f"{WEBHOOK_HOST}/{TOKEN}"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Устанавливаем вебхук при старте
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

@app.route("/", methods=["GET"])
def index():
    return "Бот работает!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
