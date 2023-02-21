from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from telegram_bot.setting.config import BOT_TOKEN
from telegram_bot.handlers.handler_main import HandlerMain


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

handlers = HandlerMain(dp)
handlers.handle()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
