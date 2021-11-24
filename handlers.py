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
mes_songs = Messages.Songs()
mes_contacts = Messages.Contacts()
mes_howto = Messages.HowTo()
mes_team = Messages.Team()


async def start_message(_):
    await bot.send_message(chat_id=config.ADMIN_CHAT, text=messages.start_polling)


async def stop_message(_):
    await bot.send_message(chat_id=config.ADMIN_CHAT, text=messages.stop_polling)


@dp.message_handler(commands='songs')
async def statuses_messages(message: types.Message):
    await message.answer('songs')


@dp.message_handler(commands='contacts')
async def statuses_messages(message: types.Message):
    await message.answer('contacts')


@dp.message_handler(commands='howto')
async def statuses_messages(message: types.Message):
    await message.answer(mes_howto.mes_text)


@dp.message_handler(commands='team')
async def statuses_messages(message: types.Message):
    await message.answer(mes_team.mes_text)


@dp.message_handler()
async def echo(message: types.Message):
    """
    Пересылаем все сообщения и айдишник юзеру, чисто для тестов
    :param message: Параметры сообщения, которое прилетело от юзера
    :return: None
    """
    if config.ENABLE_ECHO:
        await message.reply(message.text)
        await message.answer(f'usr id: {message.from_user.id}')
