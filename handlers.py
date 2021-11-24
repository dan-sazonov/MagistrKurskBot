"""
Хэндлеры бота
Этот файл может содержать функции, отвечающие за визуальное отображение и валидацию данных, тексты сообщениий должны
лежать в файле `messages.py`.
"""

import config
from aiogram import types
from dispatcher import dp, bot
from messages import Messages

messages = Messages()


async def start_message(_):
    await bot.send_message(chat_id=config.ADMIN_CHAT, text=messages.start_polling)


async def stop_message(_):
    await bot.send_message(chat_id=config.ADMIN_CHAT, text=messages.stop_polling)


@dp.message_handler()
async def echo(message: types.Message):
    """
    Пересылаем все сообщения и айдишник юзеру, чисто для тестов
    :param message: Параметры сообщения, которое прилетело от юзера
    :return: None
    """
    if not config.ENABLE_ECHO:
        return
    await message.reply(message.text)
    await message.answer(f'usr id: {message.from_user.id}')
