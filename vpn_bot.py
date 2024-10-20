import logging
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Установите уровень логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Вставьте свой токен
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот для управления VPN. Используйте /createuser для создания нового пользователя.')

async def create_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text('Используйте: /createuser <username> <password>')
        return

    username = context.args[0]
    password = context.args[1]

    try:
        # Запуск скрипта create_user.sh с параметрами result = subprocess.run(
            ['./create_user.sh'], 
            input=f"{username}\n{password}\n", 
            text=True, 
            capture_output=True
        )
        
        if result.returncode == 0:
            await update.message.reply_text(f'Пользователь {username} успешно создан.')
        else:
            await update.message.reply_text(f'Ошибка: {result.stderr}')
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: {str(e)}')

async def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("createuser", create_user))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio asyncio.run(main())
