"""
Фичи общего назначения, которые не получилось запихнуть в другие файлы
"""

import os
import random
from collections import deque

import logger

log = logger.get_logger(__name__)


def get_memes() -> str:
    """
    Возвращает путь к рандомному мемасу из заранее отобранных, или пустую строку, если мемы не найдены

    :return: путь к пикче или пустая строка
    """
    if os.path.exists('./memes'):
        memes = list(filter(lambda x: x.endswith('.jpg'), os.listdir('./memes')))
    else:
        log.warning("Directory with memes (expected ./memes/) wasn't found")
        return ''

    if os.path.exists('./logs/log_memes.txt'):
        with open('./logs/log_memes.txt', 'r') as f:
            [last_meme] = deque(f, maxlen=1) or ['']
    else:
        last_meme = 0

    while True:
        output = random.choice(memes)
        if output != last_meme:
            with open('./logs/log_memes.txt', 'w+') as f:
                f.write(output)
            break

    return os.path.join('./memes', output)


def get_username(link: str):
    pass


def find_users(name: str):
    pass
