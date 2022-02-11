from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

import config


class IsAdmin(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_owner = is_admin

    async def check(self, message: types.Message):
        return message.from_user.id in config.ADMINS_ID
