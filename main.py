import os
import logging
from flask import Flask, request, jsonify
import telebot
import requests

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError("Please set TELEGRAM_TOKEN environment variable")

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
if not WEBHOOK_URL:
    raise RuntimeError("Please set WEBHOOK_URL environment variable")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Устанавливаем webhook сразу при импорте (важно для gunicorn)
webhook_url = f"{WEBHOOK_URL.rstrip('/')}/{TOKEN}"
logging.info(f"Установка webhook на {webhook_url}")
bot.remove_webhook()
set_result = bot.set_webhook(url=webhook_url)
logging.info(f"Результат установки webhook: {set_result}")

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
        logging.info("Ответ отправлен")
    except Exception as e:
        logging.error(f"Ошибка при ответе: {e}")

@app.route("/webhook_info")
def webhook_info():
    resp = requests.get(f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo")
    return jsonify(resp.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logging.info(f"Запуск сервера на порту {port}")
    app.run(host="0.0.0.0", port=port)
