
import telebot
import threading
import time
from datetime import datetime
from flask import Flask
import os

TOKEN = "7973299304:AAGLxm6rqTJlgSNkDYx_-osYeQk7ik-hEg8"
FLIGHT_DATE = datetime(2025, 11, 2, 20, 40)

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)

# Словарь для хранения сообщений в разных чатах {chat_id: message_id}
chat_messages = {}

@app.route('/')
def home():
    return "Bot is running and updating countdown in multiple chats!"

def update_timer():
    while True:
        now = datetime.now()
        remaining = FLIGHT_DATE - now

        if remaining.total_seconds() <= 0:
            text = "✅ <b>Ты уже в пути в Таиланд! Приятного отдыха!</b>"
        else:
            days = remaining.days
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            text = (
                "✈️ <b>До вылета в Таиланд осталось:</b>\n"
                f"⏳ {days} дней {hours:02}:{minutes:02}:{seconds:02}\n\n"
                "🛫 Вылет: 2 ноября 2025, 20:40 (МСК)"
            )

        for chat_id, message_id in list(chat_messages.items()):
            try:
                bot.edit_message_text(text, chat_id, message_id, parse_mode="HTML")
            except Exception as e:
                print(f"Ошибка обновления в чате {chat_id}: {e}")

        time.sleep(60)

@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    text = "✈️ <b>До вылета в Таиланд осталось:</b>\n⏳ Загрузка таймера..."
    try:
        msg = bot.send_message(chat_id, text)
        chat_messages[chat_id] = msg.message_id
        bot.pin_chat_message(chat_id, msg.message_id, disable_notification=True)
        bot.reply_to(message, "✅ Таймер запущен!")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

def start_bot():
    t = threading.Thread(target=update_timer)
    t.daemon = True
    t.start()
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
