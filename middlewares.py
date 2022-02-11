from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class Middle(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        print(message.text)
