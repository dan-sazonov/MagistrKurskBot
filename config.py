"""
Файл с конфигами бота
Здесь задаем глобальные константы и возможно функции, настраивающие (((что-то))).
"""
import os

import logger

log = logger.get_logger(__name__)

ADMINS_ID = {385056286, 1740178046, 1202704228, 421770409, 1070984836}  # дэн, катя, миша, полина, даша
ADMIN_CHAT = 385056286  # @dan_sazonov

DEBUG_MODE = True  # режим отладки, запуск на втором домене
if DEBUG_MODE:
    log.info('Enable debug mode!')

# запрашиваем токены
req = 'DEV_TOKEN' if DEBUG_MODE else 'BOT_TOKEN'
API_TOKEN = os.getenv(req)
if not API_TOKEN:
    log.warning(f'Failed to get the {"DEV_TOKEN" if DEBUG_MODE else "BOT_TOKEN"} variable from env')
    exit(-1)

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    log.warning(f'Failed to get the DATABASE_URL variable from env')
    exit(-1)