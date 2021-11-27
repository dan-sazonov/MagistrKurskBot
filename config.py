"""
Файл с конфигами бота
Здесь задаем глобальные константы и возможно функции, настраивающие (((что-то))).
"Why not json/csv/yaml/something else? - Fuck you, here's why".
"""
import os

ADMIN_ID = {385056286, }
ADMIN_CHAT = 385056286

DB_URI = 'postgres://ykcsjuflocsgmt:9e27fa57aef50fefd7d79c80110b1a616af6ba008950655e29345e9c6def8b30@' \
         'ec2-63-32-7-190.eu-west-1.compute.amazonaws.com:5432/d3qdks4dmlesgv'

ENABLE_ECHO = False  # все команды будут попадать в эхо

# prerequisites
API_TOKEN = os.getenv('BOT_TOKEN')
if not API_TOKEN:
    exit('Err: BOT_TOKEN variable is missing')
