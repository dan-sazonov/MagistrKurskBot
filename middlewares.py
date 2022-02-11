from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

import db

db_main = db.Main()


class Middle(BaseMiddleware):
    async def on_post_process_message(self, message: types.Message, data_from_filter: list, data: dict):
        db_main.update_counter(message.from_user.id, str(message.text).lstrip('/'))
