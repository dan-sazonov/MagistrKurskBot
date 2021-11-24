"""
Создает и настраивает бота
Все, что связано с обработкой сообщений, должно быть помещено в `handlers.py`.
"""
import logging
import config

from aiogram import Bot, Dispatcher

from filters import IsOwnerFilter, IsAdminFilter, MemberCanRestrictFilter

# Configure logging
logging.basicConfig(level=logging.INFO)

# init
TOKEN = config.API_TOKEN
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# activate filters
dp.filters_factory.bind(IsOwnerFilter)
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(MemberCanRestrictFilter)
