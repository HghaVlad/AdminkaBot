from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
bot_token = config['Telegram']['Adminka_bot_token']
base_user = config['Telegram']['database_user']
base_password = config['Telegram']['database_password']
base_host = config['Telegram']['database_host']
base_db = config['Telegram']['database_name']
authen = config['Pay']['auth']

bot = Bot(bot_token, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

from filters import *
from handlers import *


async def starting(message):
    await bot.send_message(578081663, "Started")

if __name__ == '__main__':
    print("Started")
    import filters
    import handlers

    executor.start_polling(dp, on_startup=starting)
