"""
Файл с конфигами бота
Здесь задаем глобальные константы и возможно функции, настраивающие (((что-то))).
"Why not json/csv/yaml/something else? - Fuck you, here's why".
"""
import os
from aiogram import types

ADMIN_ID = {385056286, }
ADMIN_CHAT = 385056286

ENABLE_ECHO = False  # все команды будут попадать в эхо

# prerequisites
API_TOKEN = os.getenv('BOT_TOKEN')
if not API_TOKEN:
    exit('Err: BOT_TOKEN variable is missing')

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    exit('Err: DATABASE_URL variable is missing')


async def set_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('songs', 'Песенник'),
        types.BotCommand('howto', 'Как попасть на смену'),
        types.BotCommand('team', 'Педсостав центра'),
        types.BotCommand('memes', 'Получить мем'),
        types.BotCommand('contacts', 'Контакты КРОМО "Магистр"'),
        types.BotCommand('credits', 'Наша команда'),
        types.BotCommand('santa', 'Тайный Санта - регистрация'),
        types.BotCommand('help', 'Краткая справка')
    ])
