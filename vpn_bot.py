import logging
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Установите уровень логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Вставьте свой токен
TOKEN = ''

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот для управления VPN. Используйте /createuser для создания нового пользователя.')

def create_user(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 2:
        update.message.reply_text('Используйте: /createuser <username> <password>')
        return

    username = context.args[0]
    password = context.args[1]
 try:
        # Запуск скрипта create_user.sh с параметрами result = subprocess.run(['./create_user.sh'], input=f"{username}\n{password}\n", text=True, capture_output=True)
        if result.returncode == 0:
            update.message.reply_text(f'Пользователь {username} успешно создан.')
        else:
            update.message.reply_text(f'Ошибка: {result.stderr}')
    except Exception as e:
        update.message.reply_text(f'Произошла ошибка: {str(e)}')

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("createuser", create_user))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
