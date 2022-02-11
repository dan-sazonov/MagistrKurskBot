"""
Создает и настраивает бота
Все, что связано с обработкой сообщений, должно быть помещено в `handlers.py`.
"""
import logging

import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import filters
from middlewares import Middle

# прикручиваем логирование
logging.basicConfig(level=logging.INFO)

# кастомные костыльные логи TODO выпилить
if config.ENABLE_ECHO:
    print('INFO: echo mode enable')

# инит
TOKEN = config.API_TOKEN
bot = aiogram.Bot(token=TOKEN, parse_mode="HTML")
storage = MemoryStorage()

dp = aiogram.Dispatcher(bot, storage=storage)
dp.middleware.setup(Middle())
dp.bind_filter(filters.IsAdmin)
