"""
Создает и настраивает бота
Все, что связано с обработкой сообщений, должно быть помещено в `handlers.py`.
"""

import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import filters
import logger
import logging
# from middlewares import Middle

# логирование
logging.basicConfig(level=logging.INFO)

# инит
TOKEN = config.API_TOKEN
bot = aiogram.Bot(token=TOKEN, parse_mode="HTML")
storage = MemoryStorage()

dp = aiogram.Dispatcher(bot, storage=storage)
# dp.middleware.setup(Middle())
dp.bind_filter(filters.IsAdmin)
