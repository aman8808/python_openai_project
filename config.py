import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

# Получение URL базы данных из переменной окружения
DATABASE_URL = os.getenv('DATABASE_URL')

# Получение OpenAI API ключа из переменной окружения
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Настройка конфигурации базы данных
DATABASE_CONFIG = {
    'url': DATABASE_URL
}

# Вывод конфигурации для проверки (не рекомендуется в продакшене)
print("Database URL:", DATABASE_CONFIG['url'])
print("OpenAI API Key:", OPENAI_API_KEY)
