"""
Хэндлеры бота
Этот файл может содержать функции, отвечающие за визуальное отображение и валидацию данных, тексты сообщениий должны
лежать в файле `messages.py`.
"""
from aiogram import types

import config
import db
import features
from dispatcher import dp, bot, storage
from messages import Messages, Keyboards

messages = Messages()
keyboards = Keyboards()
db_main = db.Main()


async def on_startup(_):
    await bot.send_message(chat_id=config.ADMIN_CHAT, text=messages.start_polling)


async def on_shutdown(_):
    await bot.close()
    await storage.close()
    await bot.send_message(chat_id=config.ADMIN_CHAT, text=messages.stop_polling)


@dp.message_handler(commands=['songs'])
async def songs_mes(message: types.Message):
    await message.answer(messages.songs, reply_markup=keyboards.get_songs_kb())


@dp.message_handler(commands=['contacts'])
async def contacts_mes(message: types.Message):
    await message.answer(messages.contacts, reply_markup=keyboards.get_contacts_kb())


@dp.message_handler(commands=['howto'])
async def howto_mes(message: types.Message):
    await message.answer(messages.howto)


@dp.message_handler(commands=['team'])
async def team_mes(message: types.Message):
    await message.answer(messages.team)


@dp.message_handler(commands=['memes'])
async def memes_mes(message: types.Message):
    out = features.get_memes()
    if out:
        await message.answer_photo(types.InputFile(out))
    else:
        await message.answer('Мемов нет(')


@dp.message_handler(commands=['credits'])
async def memes_mes(message: types.Message):
    await message.answer(messages.credit, disable_web_page_preview=True)


@dp.message_handler(commands=['subscribe', 'start'])
async def start_mes(message: types.Message):
    await message.answer(messages.subscribe)
    await message.answer(messages.do_unsubscribe)
    db_main.add_user(int(message.from_user.id), message.from_user.username)


@dp.message_handler(commands=['unsubscribe', 'stop'])
async def stop_mes(message: types.Message):
    db_main.del_user(int(message.from_user.id))
    await message.answer(messages.unsubscribe)
    await message.answer(messages.do_subscribe)


@dp.message_handler(commands=['help', '!', '?'])
async def help_mes(message: types.Message):
    await message.answer(messages.help, disable_web_page_preview=True)


@dp.message_handler(commands=['santa', 'end'])
async def outdated_mes(message: types.Message):
    await message.answer(messages.placeholder)


@dp.callback_query_handler(lambda c: c.data in {'not_rcd', 'start_pol', 'received_btn', 'sent_btn'})
async def outdated_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, text='¯\\_(ツ)_/¯', show_alert=True)


@dp.message_handler(commands=['test'])
async def outdated_mes(message: types.Message):
    await bot.send_message(565656, 'fuck')


@dp.message_handler()
async def unknown_command_mes(message: types.Message):
    await message.reply(messages.not_command)
