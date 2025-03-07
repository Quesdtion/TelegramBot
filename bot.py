import os
import openai
import telebot
import git
from github import Github
from datetime import datetime

# Вставьте ваш API ключ OpenAI и Telegram
openai.api_key = "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"  # Ваш OpenAI API ключ
API_TOKEN = "7671376837:AAGgp6Vyz2o-IcviYljQz409QQZq-3V5ztI"  # Ваш Telegram Bot API токен
GITHUB_TOKEN = "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"  # Ваш GitHub Token, который вы получите на GitHub
REPO_NAME = "Quesdtion/TelegramBot"  # Название вашего репозитория на GitHub, например "username/repository_name"
COMMIT_MESSAGE = "Automated code generation commit"

bot = telebot.TeleBot(API_TOKEN)

# Функция для генерации кода через OpenAI
def generate_code(prompt):
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Ошибка при взаимодействии с OpenAI: {e}")
        return "Произошла ошибка при генерации кода."

# Функция для коммита кода в GitHub
def commit_to_github(code):
    try:
        # Инициализация GitHub API
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)

        # Создание нового файла с сгенерированным кодом
        file_name = f"generated_code_{datetime.now().strftime('%Y%m%d%H%M%S')}.py"
        with open(file_name, "w") as file:
            file.write(code)

        # Коммит и push в GitHub
        repo.create_file(file_name, COMMIT_MESSAGE, code, branch="main")
        print(f"Файл {file_name} успешно закоммичен в репозиторий {REPO_NAME}.")
    except Exception as e:
        print(f"Ошибка при коммите в GitHub: {e}")

# Обработчик команд в Telegram
@bot.message_handler(commands=['generate_code'])
def handle_generate_code(message):
    bot.send_message(message.chat.id, "Отправьте описание для генерации кода.")

# Обработчик обычных сообщений (генерация кода)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    prompt = message.text
    bot.send_message(message.chat.id, "Генерация кода... Пожалуйста, подождите.")
    
    # Генерация кода с помощью OpenAI
    code = generate_code(prompt)
    
    # Отправка сгенерированного кода пользователю
    bot.send_message(message.chat.id, f"Сгенерированный код:\n```python\n{code}\n```", parse_mode="Markdown")
    
    # Автоматический коммит кода в GitHub
    commit_to_github(code)

# Запуск бота
bot.polling()
