from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from dispatcher import dp, bot, storage
from dispatcher import dp, bot
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from aiogram.dispatcher import FSMContext


def init():
    pass


class Polling(StatesGroup):
    Start = State()


@dp.message_handler(commands=['valentine'])
async def memes_mes(message: types.Message):
    btn_1 = types.InlineKeyboardButton('U+2764', callback_data='start_btn')
    kb = types.InlineKeyboardMarkup().add(btn_1)
    await message.answer('''Привет! Ты попал в меню "Тайный Валентин"!

Здесь ты можешь отправить письмо или валентинку любому человеку, ведь сегодня – День святого Валентина – нужно делиться своими чувствами в такие непростые времена U+1F496

Нажми кнопку "U+2764", чтобы начать''', reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data == 'start_btn')
async def start_polling(callback_query: types.CallbackQuery):
    btn_1 = types.InlineKeyboardButton('U+2764', callback_data='letter')
    btn_2 = types.InlineKeyboardButton('U+2764', callback_data='sticker')
    kb = types.InlineKeyboardMarkup().add(btn_1).add(btn_2)

    uid = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(uid, '''Отлично, приступим!
Что ты хочешь отправить?''', reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data == 'letter', state=None)
async def answer_q1(callback_query: types.CallbackQuery, state: FSMContext):
    uid = callback_query.from_user.id
    await state.update_data(type='letter')
    await state.update_data(uid=uid)

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(uid, '''Письмо''')
    await Polling.Start.set()


@dp.callback_query_handler(lambda c: c.data == 'sticker', state=None)
async def answer_q1(callback_query: types.CallbackQuery, state: FSMContext):
    uid = callback_query.from_user.id
    await state.update_data(type='sticker')
    await state.update_data(uid=uid)

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(uid, '''Стикер''')
    await Polling.Start.set()
