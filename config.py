"""
Файл с конфигами бота
Здесь задаем глобальные константы и возможно функции, настраивающие (((что-то))).
"Why not json/csv/yaml/something else? - Fuck you, here's why".
"""
import os

ADMIN_ID = {385056286, }
ADMIN_CHAT = 385056286

# prerequisites
API_TOKEN = os.getenv('BOT_TOKEN')
if not API_TOKEN:
    exit('Err: BOT_TOKEN variable is missing')
