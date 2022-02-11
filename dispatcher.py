"""
Создает и настраивает бота
Все, что связано с обработкой сообщений, должно быть помещено в `handlers.py`.
"""
import logging

import aiogram
from middlewares import Middle
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

# Configure logging
logging.basicConfig(level=logging.INFO)

# кастомные костыльные логи
if config.ENABLE_ECHO:
    print('INFO: echo mode enable')

# init
TOKEN = config.API_TOKEN
bot = aiogram.Bot(token=TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = aiogram.Dispatcher(bot, storage=storage)
dp.middleware.setup(Middle())
