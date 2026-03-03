# Telegram Analytics Bot (FastAPI + PostgreSQL + aiogram)

## Возможности
- Подсчёт общего количества видео  
- Фильтрация по creator_id  
- Фильтрация по диапазону дат  
- Фильтрация по порогу просмотров  
- Подсчёт прироста просмотров (delta_views_count)  
- Асинхронная работа  
- LLM-провайдер: `fake` или `openai`

##  Установка и запуск

### 1. Клонировать репозиторий
- git clone https://github.com/Alex-Domini/analytics-bot
- cd analytics-bot


### 2. Создать виртуальное окружение
- python -m venv .venv
- .venv\Scripts\activate


### 3. Установить зависимости
pip install -r requirements.txt


## Настройка переменных окружения
### Создать файл .env:
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=password
- POSTGRES_HOST=localhost
- POSTGRES_PORT=5432
- POSTGRES_DB=analytics

- BOT_TOKEN=your_telegram_bot_token

- LLM_PROVIDER=openai
- OPENAI_API_KEY=your_api_key

## LLM-провайдер выбирается через .env:
- LLM_PROVIDER=fake
- LLM_PROVIDER=openai

## Миграции
- alembic upgrade head

## Как подготовить данные:
1. Перейдите в раздел **[Releases](https://github.com/Alex-Domini/analytics-bot/releases/tag/v1.0.0)**.
2. В блоке **Assets** скачайте файл `videos.json`.
3. Положите скачанный файл в корневую папку проекта

## Загрузка данных из JSON
- python -m app.main

## Запуск Telegram-бота
- python -m app.bot

## Небольшой список вопросов для Телеграм-бота
- Какое суммарное количество просмотров набрали все видео, опубликованные в июне 2025 года?
- число просмотров за час оказалось отрицательным
- Сколько всего видео загружено в систему
- Сколько видео набрало больше 10 000 просмотров за всё время
- Сколько видео у креатора aca1061a9d324ecf8c3fa2bb32d7be63 вышло с 1 по 20 ноября 2025?

## Архитектура
 Telegram → NL Parser → AnalyticsRequest → SQLExecutor → PostgreSQL

## Telegram-слой
- реализован через aiogram
- полностью асинхронный
- один запрос → один ответ
- контекст диалога не хранится
## Преобразование текстового запроса
### Используется детерминированный парсер:
- регулярные выражения
- извлечение чисел
- dateparser для распознавания дат
- ключевые слова для определения метрики
## Результат парсинга — объект **AnalyticsRequest (Pydantic model).**

## Также можно использовать OpenAI:
- отправляется system prompt
- модель возвращает строго JSON
- JSON валидируется через Pydantic

## Выполнение SQL-запросов
### Компонент SQLExecutor строит ORM-запросы (SQLAlchemy 2.x async):
- count(*)
- sum(delta_views_count)
- фильтрация по creator_id
- фильтрация по датам
- views_count > threshold
- count(distinct video_id)

#### Все операции выполняются через AsyncSession + asyncpg.