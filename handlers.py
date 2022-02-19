"""
Хэндлеры бота
Этот файл может содержать функции, отвечающие за визуальное отображение и валидацию данных, тексты сообщениий должны
лежать в файле `messages.py`.
"""

import aiogram.dispatcher.filters as dp_filters
from aiogram import types

import config
import db
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
    out = db_main.get_random_meme()
    if out:
        await message.answer_photo(out)
    else:
        await message.answer('Мемов нет(')


@dp.message_handler(commands=['credits'])
async def memes_mes(message: types.Message):
    await message.answer(messages.credit, disable_web_page_preview=True)


@dp.message_handler(dp_filters.CommandStart())
async def start_mes(message: types.Message):
    await message.answer(messages.subscribe)
    await message.answer(messages.do_unsubscribe)
    db_main.add_user(int(message.from_user.id), message.from_user.username, tuple(message.from_user.full_name.split()))
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
    await message.answer(messages.placeholder_santa)


@dp.message_handler(commands=['valentine'])
async def step_0(message: types.Message):
    await message.answer(messages.placeholder_valentine)


@dp.callback_query_handler(
    lambda c: c.data in {'not_rcd', 'start_pol', 'received_btn', 'sent_btn', 'start_btn', 'letter', 'sticker',
                         'title_true', 'title_false', 'send', 'abort'})
async def outdated_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, text='¯\\_(ツ)_/¯', show_alert=True)
    log.info(f'The user clicked on an outdated button: {callback_query.id}')


@dp.message_handler(is_admin=True, commands=['test'])
async def test_state(message: types.Message):
    log.info(f'`{message.from_user.id}` asked the state of the bot')
    await message.answer(f'''🔔 <b>Все прекрасно!</b>
Информация о тебе:
id: {message.from_user.id}
юзернейм: {message.from_user.username}
имя: {message.from_user.first_name}
фамилия: {message.from_user.last_name}''')


@dp.message_handler(is_admin=True, commands=['disable'])
async def disable_bot(message: types.Message):
    log.info(f'`{message.from_user.id}` stopped the bot')
    await message.answer('🔔 Бот будет остановлен')
    await on_shutdown(None)


@dp.message_handler(content_types=['photo'])
async def scan_message(msg: types.Message):
    document_id = msg.photo[0].file_id
    file_info = await bot.get_file(document_id)
    await msg.reply(f'''file_id: {file_info.file_id}
file_path: {file_info.file_path}''')


@dp.message_handler(is_admin=True, commands=['get'])
async def test_state(message: types.Message):
    file = message.text.split(' ')[-1]
    log.info(f'`{message.from_user.id}` asked the {file} log')

    if file in {'main', 'updates', 'warnings'}:
        await message.answer(logger.get_last_logs(file))
    else:
        log.info(f'Incorrect argument in /get command: {file}')
        await message.answer('Неправильная команда. Чтобы посмотреть все варианты, вызови /admin')


@dp.message_handler(is_admin=True, commands=['admin'])
async def test_state(message: types.Message):
    log.info(f'`{message.from_user.id}` asked the admin commands list')
    await message.answer('''Это список секретных команд, которые доступны только админам канала. По мере развития бота их список будет пополнятся.

/admin - покажет это сообщение
/test - быстрая проверка работоспособности бота
/disable - принудительная остановка бота
/get <i>что-то</i> - выгрузит последние 5 строк отчета. Вместо <i>"что-то"</i> надо написать что-то из этого:
    <code>main</code> - полный отчет о работе
    <code>updates</code> - сообщения и нажатия кнопок, которые прилетели от пользователей
    <code>warnings</code> - критические ошибки

Вывод команды <code>get</code> пока что выглядит крайне ужасно, но в обозримом будущем ему будет придан более симпатичный вид.''')


@dp.message_handler()
async def unknown_command_mes(message: types.Message):
    await message.reply(messages.not_command)
