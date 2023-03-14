import os
import logging
import telegram
from pytube import YouTube
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Получаем токен бота из переменной окружения
TOKEN = 'Token'

# Создаем экземпляр класса Updater
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Обработчик команды start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот, который может скачивать видео с YouTube. Просто отправь мне ссылку на видео, и я отправлю его тебе в личном сообщении.")

# Обработчик сообщений с ссылками на видео
def download_video(update, context):
    message_text = update.message.text
    chat_id = update.effective_chat.id

    # Проверяем, является ли сообщение ссылкой на YouTube видео
    if 'youtube.com' in message_text or 'youtu.be' in message_text:
        try:
            # Скачиваем видео
            yt = YouTube(message_text)
            stream = yt.streams.get_highest_resolution()
            stream.download()
            file_name = stream.default_filename

            # Отправляем видео в личном сообщении
            context.bot.send_video(chat_id=chat_id, video=open(file_name, 'rb'))
            os.remove(file_name)  # Удаляем загруженный файл

        except Exception as e:
            logging.error(str(e))
            context.bot.send_message(chat_id=chat_id, text="Произошла ошибка при загрузке видео. Попробуйте еще раз.")
    else:
        context.bot.send_message(chat_id=chat_id, text="Я могу загрузить только видео с YouTube. Пожалуйста, отправьте ссылку на YouTube видео.")

# Добавляем обработчики команд и сообщений
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

download_video_handler = MessageHandler(Filters.text & (~Filters.command), download_video)
dispatcher.add_handler(download_video_handler)

# Запускаем бота
updater.start_polling()
