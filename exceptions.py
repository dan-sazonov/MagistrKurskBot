"""
Хэндлеры для обработки исключений
"""

import aiogram.utils.exceptions as exc
from aiogram import types

from dispatcher import dp


@dp.errors_handler
async def errors_handler(update: types.Update, exception: exc.TelegramAPIError):
    if isinstance(exception, exc.CantParseEntities):
        print(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, exc.BadRequest):
        print(f'BadRequest: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, exc.TelegramAPIError):
        print(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True

    print(f'Update: {update} \n{exception}')
