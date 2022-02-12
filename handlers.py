"""
Хэндлеры бота
Этот файл может содержать функции, отвечающие за визуальное отображение и валидацию данных, тексты сообщениий должны
лежать в файле `messages.py`.
"""
import os

import aiogram.dispatcher.filters as dp_filters
from aiogram import types

import config
import db
import features
import logger
from dispatcher import dp, bot, storage
from messages import Messages, Keyboards

log = logger.get_logger(__name__)

messages = Messages()
keyboards = Keyboards()
db_main = db.Main()


async def on_startup(_):
    log.info('Start polling')
    await bot.send_message(chat_id=config.ADMIN_CHAT, text=messages.start_polling)


async def on_shutdown(_):
    log.info('Stop polling')
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


@dp.message_handler(dp_filters.CommandStart())
async def start_mes(message: types.Message):
    await message.answer(messages.subscribe)
    await message.answer(messages.do_unsubscribe)
    db_main.add_user(int(message.from_user.id), message.from_user.username)
    log.info(f'A new user has joined: {message.from_user.id}')


@dp.message_handler(commands=['unsubscribe', 'stop'])
async def stop_mes(message: types.Message):
    log.info(f'The user has left the bot: {message.from_user.id}')
    await message.answer(messages.unsubscribe)
    await message.answer(messages.do_subscribe)
    db_main.del_user(int(message.from_user.id))


@dp.message_handler(dp_filters.CommandHelp())
async def help_mes(message: types.Message):
    await message.answer(messages.help, disable_web_page_preview=True)


@dp.message_handler(commands=['santa', 'end'])
async def outdated_mes(message: types.Message):
    await message.answer(messages.placeholder)


@dp.callback_query_handler(lambda c: c.data in {'not_rcd', 'start_pol', 'received_btn', 'sent_btn'})
async def outdated_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, text='¯\\_(ツ)_/¯', show_alert=True)
    log.info(f'The user clicked on an outdated button: {callback_query.id}')


@dp.message_handler(is_admin=True, commands=['test'])
async def test_state(message: types.Message):
    log.info(f'`{message.from_user.id}` asked the state of the bot')
    await message.answer('🔔 Все прекрасно!')


@dp.message_handler(is_admin=True, commands=['disable'])
async def disable_bot(message: types.Message):
    log.info(f'`{message.from_user.id}` stopped the bot')
    await message.answer('🔔 Бот будет остановлен')
    await on_shutdown(None)


@dp.message_handler(is_admin=True, commands=['get_updates'])
async def test_state(message: types.Message):
    log.info(f'`{message.from_user.id}` asked the updates log')
    if not os.path.exists('./logs/updates.log'):
        log.warning(f"File `./logs/updates.log` wasn't found")
        await message.answer('Что-то пошло не так, и этот файл исчез прямо на глазах😐')

    with open('./logs/updates.log', 'r') as f:
        await message.answer('\n'.join(f.readlines()[-15:]))


@dp.message_handler()
async def unknown_command_mes(message: types.Message):
    await message.reply(messages.not_command)
