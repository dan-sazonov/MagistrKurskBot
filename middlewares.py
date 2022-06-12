"""
Обработка апдейтов на мидлваре
"""


from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

import db
import logger

log = logger.get_updates_logger()
db_main = db.Main()


class Middle(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        """
        Логируем прилетающие апдейты.
        """
        log.info(update)

    async def on_post_process_message(self, message: types.Message, data_from_filter: list, data: dict):
        """
        Увеличиваем счетчик сообщений для юзера. Неиспользуемые параметры не выкидывать!
        """
        db_main.update_counter(message.from_user.id, str(message.text).lstrip('/'))
