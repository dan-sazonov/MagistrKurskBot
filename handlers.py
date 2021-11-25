"""
Хэндлеры бота
Этот файл может содержать функции, отвечающие за визуальное отображение и валидацию данных, тексты сообщениий должны
лежать в файле `messages.py`.
"""

import config
import dispatcher

from dispatcher import dp, bot
from messages import Messages
from aiogram import types

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
async def process_command_1(message: types.Message):
    await message.answer(mes_songs.mes_text, reply_markup=dispatcher.songs_kb)


@dp.message_handler(commands='contacts')
async def statuses_messages(message: types.Message):
    await message.answer(mes_contacts.mes_text, reply_markup=dispatcher.contacts_kb)


@dp.message_handler(commands='howto')
async def statuses_messages(message: types.Message):
    await message.answer(mes_howto.mes_text)


@dp.message_handler(commands='team')
async def statuses_messages(message: types.Message):
    await message.answer(mes_team.mes_text)


@dp.message_handler(commands=['subscribe', 'start'])
async def statuses_messages(message: types.Message):
    # todo добавляем чела в бд к активным, если его там еще нет
    await message.answer(messages.subscribe)
    await message.answer(messages.do_unsubscribe)


@dp.message_handler(commands=['unsubscribe', 'stop'])
async def statuses_messages(message: types.Message):
    # todo удалем чела из активных, если он еще там
    await message.answer(messages.unsubscribe)
    await message.answer(messages.do_subscribe)


@dp.message_handler(commands=['help', '!', '?'])
async def statuses_messages(message: types.Message):
    await message.answer(messages.help)


@dp.message_handler()
async def echo(message: types.Message):
    """
    Пересылаем все сообщения и айдишник юзеру, чисто для тестов
    Если эхо выключено, шлем сообщение, что команда не понятна
    :param message: Параметры сообщения, которое прилетело от юзера
    :return: None
    """
    if config.ENABLE_ECHO:
        await message.reply(message.text)
        await message.answer(f'usr id: {message.from_user.id}')
    else:
        await message.reply(messages.not_command)
