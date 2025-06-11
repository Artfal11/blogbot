import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from app.config import BOT_TOKEN, API_URL

logging.basicConfig(level=logging.INFO)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Напиши /posts, чтобы увидеть список постов.")


def posts(update: Update, context: CallbackContext):
    try:
        resp = requests.get(f"{API_URL}/posts/")
        resp.raise_for_status()
    except Exception as e:
        logging.error(f"Ошибка запроса к API: {e}")
        update.message.reply_text("Ошибка при получении постов с сервера.")
        return

    posts = resp.json()

    if not posts:
        update.message.reply_text("Постов пока нет.")
        return

    keyboard = [
        [InlineKeyboardButton(text=post["title"], callback_data=str(post["id"]))]
        for post in posts
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите пост:", reply_markup=reply_markup)


def post_detail(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    post_id = query.data
    try:
        resp = requests.get(f"{API_URL}/posts/{post_id}")
        resp.raise_for_status()
    except Exception as e:
        logging.error(f"Ошибка получения поста: {e}")
        query.edit_message_text("Не удалось загрузить пост.")
        return

    post = resp.json()
    text = f"📝 <b>{post['title']}</b>\n\n{post['content']}\n\n🗓 {post['created_at']}"
    query.edit_message_text(text=text, parse_mode="HTML")


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("posts", posts))
    dp.add_handler(CallbackQueryHandler(post_detail))

    logging.info("Бот запущен...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
