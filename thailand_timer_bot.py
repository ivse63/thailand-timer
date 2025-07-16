
import telebot
import threading
import time
from datetime import datetime

TOKEN = "7973299304:AAGLxm6rqTJlgSNkDYx_-osYeQk7ik-hEg8"
CHAT_ID = -1001432031599  # Числом, Telebot нормально работает с int
MESSAGE_ID = None

FLIGHT_DATE = datetime(2025, 11, 2, 20, 40)

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

def update_timer():
    global MESSAGE_ID
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

        try:
            if MESSAGE_ID is None:
                msg = bot.send_message(CHAT_ID, text)
                MESSAGE_ID = msg.message_id
                bot.pin_chat_message(CHAT_ID, MESSAGE_ID, disable_notification=True)
            else:
                bot.edit_message_text(text, CHAT_ID, MESSAGE_ID, parse_mode="HTML")
        except Exception as e:
            print(f"Ошибка обновления: {e}")

        time.sleep(60)

def start_timer_thread():
    t = threading.Thread(target=update_timer)
    t.daemon = True
    t.start()

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "✅ Таймер запущен! Сообщение закреплено и будет обновляться каждые 60 секунд.")

if __name__ == "__main__":
    start_timer_thread()
    bot.infinity_polling()
