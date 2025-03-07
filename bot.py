import asyncio
import signal
import csv
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = 'YOUR_BOT_TOKEN_HERE'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Имя файла для сохранения данных
CSV_FILE = "collected_data.csv"

# Функция для записи в CSV файл
def save_to_csv(data):
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Пример обработчика текстовых сообщений
@dp.message_handler()
async def collect_data(message: types.Message):
    # Сохранение данных в CSV
    data = [message.from_user.id, message.from_user.username, message.text]
    save_to_csv(data)
    await message.reply("Ваше сообщение было сохранено.")

# Функция для корректного завершения работы
def shutdown(loop):
    loop.stop()
    print("Бот завершил работу.")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    # Регистрация обработчиков сигналов
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: shutdown(loop))

    # Запуск бота
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        loop.close()
