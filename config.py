"""
Файл с конфигами бота
Здесь задаем глобальные константы и возможно функции, настраивающие (((что-то))).
"""
import os

ADMINS_ID = {385056286, 1740178046, 1202704228, 421770409, 1070984836}  # дэн, катя, миша, полина, даша
ADMIN_CHAT = 385056286  # @dan_sazonov

ENABLE_ECHO = False  # все команды будут попадать в эхо
DEBUG_MODE = True  # режим отладки, запуск на втором домене

# запрашиваем токены
req = 'DEV_TOKEN' if DEBUG_MODE else 'BOT_TOKEN'
API_TOKEN = os.getenv(req)
if not API_TOKEN:
    exit('Err: BOT_TOKEN variable is missing')

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    exit('Err: DATABASE_URL variable is missing')
