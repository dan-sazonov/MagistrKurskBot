"""
Хэндлеры для обработки исключений
"""

import aiogram.utils.exceptions as exc
from aiogram import types

import logger
from dispatcher import dp

log = logger.get_logger(__name__)


class AiogramExc:
    @dp.errors_handler()
    async def errors_handler(self: types.Update, exception: exc.TelegramAPIError):
        log.warning(f"Uncaught exception: {exception}. update_id: {self['update_id']}")
        return True
