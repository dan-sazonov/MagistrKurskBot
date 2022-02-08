"""
Хэндлеры для обработки исключений
"""

import aiogram.utils.exceptions as exc
from aiogram import types

from dispatcher import dp


class CustomExc:
    @dp.errors_handler(exception=exc.ChatNotFound)
    async def errors_handler(self: types.Update, exception: exc.TelegramAPIError):
        msg = f'{exception} \nUpdate: {self}'
        print(msg)
        return True
