"""
Хэндлеры для обработки исключений
"""

import aiogram.utils.exceptions as exc
from aiogram import types

from dispatcher import dp


class AiogramExc:
    @dp.errors_handler(exception=exc.ChatNotFound)
    async def errors_handler(self: types.Update, exception: exc.TelegramAPIError):
        msg = f"{exception}. This exception was't caught with `try`. update_id: {self['update_id']}"
        print(msg)
        return True
