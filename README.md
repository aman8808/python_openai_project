      FastAPI RAG API (РУКОВОДСТВО ПО ЭКСПЛУАТАЦИИ АВТОМОБИЛЯ)

Этот проект реализует API для поиска релевантной информации с использованием 
Retrieval-Augmented Generation (RAG) и OpenAI API. 
API позволяет принимать текстовые запросы от пользователей,
искать релевантные данные, генерировать ответы на основе найденной информации
и OpenAI, а также сохранять запросы и ответы в базе данных.

 Функции

1) Генерация ответа: Принимает текстовый запрос от пользователя и возвращает сгенерированный ответ.
2) Поиск релевантных данных: Извлекает векторы из загруженных документов и использует их для поиска релевантной информации.
3) Интеграция с OpenAI API: Отправляет запросы в OpenAI API для генерации ответа на основе контекста из найденных данных.
4) Хранение данных: Сохраняет запросы и ответы в базе данных PostgreSQL с использованием расширения pgvector.
5) Установка и настройка

    Требования

- Python 3.9+
- PostgreSQL с расширением pgvector
- Docker и Docker Compose (для развертывания в контейнерах)

                Установка 
  - Клонируйте репозиторий с гитхаб и следуйте инструкциям

    


                Файл config.py


DATABASE_CONFIG = {
    'dbname': 'ваша база',
    'user': 'логин',
    'password': 'ваш пароль',
    'host': 'localhost',
    'port': '5432'
}


DATABASE_URL=postgresql://amankarabalaev:mypassword@localhost:5432/my_vectorbd
OPENAI_API_KEY = 'добавьте свой ключ Чат GPT' (мой хранится в .env)


            СОЗДАНИЕ БД
createdb -U amankarabalaev -h localhost -p 5432 my__vectorbd


            ВОССТАНОВЛЕНИЕ БД ИЗ ДАМПА
psql -U amankarabalaev -h localhost -p 5432 -d my__vectorbd -f database_backup.sql




              Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



            docker-compose.yml



version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: my_vectorbd
      POSTGRES_USER: amankarabalaev
      POSTGRES_PASSWORD: mypassword
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:


                    ПРИМЕРЫ ЗАПРОСОВ:

curl -X POST http://localhost:8080/generate-response/ \
-H "Content-Type: application/json" \
-d '{"query": " допустима установка самодельной перемычки или предохранителя 
другого номинала взамен перегоревшего?"}'


Ответ - Заменять перегоревший предохранитель на самодельную перемычку или 
предохранитель другого номинала категорически не рекомендуется. 
Предохранитель служит для защиты электрической цепи от перегрузок и коротких
замыканий. Перемычка или предохранитель неподходящего номинала не обеспечит 
должной защиты, что может привести к повреждению оборудования или возникновению
пожара


curl -X POST http://localhost:8080/generate-response/ \
-H "Content-Type: application/json" \
-d '{"query": " Чтобы не появились пятна на лакокрасочном покрытии под 
люком топливного бака при попадании бензин нужно?"}'


Ответ - Прежде всего, следует быть аккуратным при заправке автомобиля, чтобы 
избежать брызг бензина на краску. Если же бензин все же попал на лакокрасочное
покрытие, его следует немедленно протереть, используя чистую ветошь или ткань.