import os
from flask import Flask, request
import telebot
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError("Please set TELEGRAM_TOKEN environment variable")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    logging.info(f"Получено сообщение: {message.text} от {message.from_user.id}")
    try:
        bot.reply_to(message, message.text)
    except Exception as e:
        logging.error(f"Ошибка при ответе: {e}")

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
if WEBHOOK_URL:
    webhook_url = f"{WEBHOOK_URL.rstrip('/')}/{TOKEN}"
    bot.remove_webhook()
    result = bot.set_webhook(url=webhook_url)
    logging.info(f"Установка webhook на {webhook_url}: {result}")
else:
    logging.warning("WEBHOOK_URL не задан")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logging.info(f"Запуск сервера на порту {port}")
    app.run(host="0.0.0.0", port=port)
