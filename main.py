import os
import logging
from flask import Flask, request
import telebot

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

webhook_url = f"{WEBHOOK_URL.rstrip('/')}/{TOKEN}"
bot.remove_webhook()
bot.set_webhook(url=webhook_url)

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=['start'])
def start(message):
    logging.info(f"Получена команда /start от {message.from_user.id}")
    bot.reply_to(message, "Привет! Бот работает.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
