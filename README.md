# Telegram Blog Bot

## Стек

- FastAPI + SQLite (API)
- python-telegram-bot (бот)

## Установка

```bash
git clone https://github.com/Artfal11/blogbot.git
cd blogbot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## .env файл

- Дублируем .env.example и переименовываем в .env
- Вставляем свой BOT_TOKEN

## Запуск FastAPI и тг-бота

```bash
uvicorn app.main:app --reload

PYTHONPATH=. python bot/bot.py
```