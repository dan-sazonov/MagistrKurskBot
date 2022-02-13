from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

import config


class IsAdmin(BoundFilter):
    """
    Проверяет, есть ли чел в списке админов. Список админов в config.ADMINS_ID, по дефолту там все 7
    """
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_owner = is_admin

    async def check(self, message: types.Message) -> bool:
        return message.from_user.id in config.ADMINS_ID
