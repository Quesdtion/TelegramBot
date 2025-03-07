# openai_api.py

import openai

openai.api_key = "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"

async def chat_with_ai(report):
    try:
        # Новый API-метод для общения с ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # или другой доступный модел
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": report},
            ],
        )
        return response['choices'][0]['message']['content']

    except Exception as e:
        print(f"Ошибка при взаимодействии с AI: {e}")
        return "Произошла ошибка при взаимодействии с ИИ."
