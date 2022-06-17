"""
Создает и настраивает бота
Все, что связано с обработкой сообщений, должно быть раскидано по модулям в зависимости от уровня
"""

import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import filters
import logger
from middlewares import Middle

# логирование
logger.set_basic_logger()

# инит
TOKEN = config.API_TOKEN
bot = aiogram.Bot(token=TOKEN, parse_mode="HTML")
storage = MemoryStorage()

dp = aiogram.Dispatcher(bot, storage=storage)
dp.middleware.setup(Middle())

# биндим фильтры
dp.bind_filter(filters.IsAdmin)
