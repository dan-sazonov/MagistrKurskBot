import random
import os
from collections import deque


def get_memes():
    """
    Возвращает рандомный мемас из заранее отобранных
    :return: путь к пикче
    """
    memes = []
    if os.path.exists('./memes'):
        memes = list(filter(lambda x: x.endswith('.jpg'), os.listdir('./memes')))

    if not memes:
        raise FileNotFoundError('./memes dir not found')

    with open('memes/log_memes.txt', 'r') as f:
        [last_meme] = deque(f, maxlen=1) or ['']

    while True:
        output = random.choice(memes)
        if output != last_meme:
            with open('memes/log_memes.txt', 'w') as f:
                f.write(output)
            break

    return os.path.join('./memes', output)
