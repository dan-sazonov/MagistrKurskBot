"""
Хэндлеры для обработки исключений
"""

import aiogram.utils.exceptions as exc
from aiogram import types

from dispatcher import dp


@dp.errors_handler(exception=exc.TelegramAPIError)
async def error_bot_blocked(update: types.Update, exception: exc.TelegramAPIError):
    print(f'сообщение: {update}, ошибка: {exception}')
    print('тiкай, бачек потик')
    return True
