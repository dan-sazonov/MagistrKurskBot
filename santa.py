from dispatcher import dp, bot
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from aiogram.dispatcher import FSMContext
from messages import Messages
from db import Santa, Main, Drawing


def init():
    # костыль, чтобы импорт в handlers.py не был пустым
    pass


messages = Messages()
mes_santa = Messages.Santa()
db = Santa()
db_main = Main()
db_drawing = Drawing()


class Poll(StatesGroup):
    Wishes = State()
    OnMeeting = State()
    Address = State()
    Name = State()


@dp.message_handler(commands=['santa_'], state=None)
async def start_polling(message: types.Message):
    await message.answer(mes_santa.on_start, disable_web_page_preview=True)
    await message.answer(mes_santa.ask_wishes)
    db_main.update_counter(message.from_user.id, 'santa')

    await Poll.Wishes.set()


@dp.message_handler(state=Poll.Wishes)
async def answer_q1(message: types.Message, state: FSMContext):
    mes_kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_1 = types.KeyboardButton('Да!')
    btn_2 = types.KeyboardButton('Нет')
    mes_kb.row(btn_1, btn_2)

    answer = message.text
    await state.update_data(wishes=answer)

    await message.answer(mes_santa.ask_meeting, reply_markup=mes_kb)
    await Poll.OnMeeting.set()


@dp.message_handler(state=Poll.OnMeeting)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    if answer not in ['Да!', 'Нет']:
        await message.reply('Я тебя не понял. Пожалуйста, используй кнопки для ответа')
        return
    answer = {'Да!': True, 'Нет': False}[answer]
    await state.update_data(on_meeting=answer)

    await message.answer(mes_santa.ask_address, reply_markup=types.ReplyKeyboardRemove())
    await Poll.Address.set()


@dp.message_handler(state=Poll.Address)
async def answer_q3(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(address=answer)

    await message.answer(mes_santa.ask_name)
    await Poll.Name.set()


@dp.message_handler(state=Poll.Name)
async def answer_q3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    form = {'wishes': data.get("wishes"), 'on_meeting': data.get("on_meeting"), 'address': data.get("address"),
            'name': message.text}

    db.add_user(int(message.from_user.id), form)

    await message.answer(mes_santa.on_end)
    await state.finish()


@dp.message_handler(commands=['end_'])
async def team_mes(message: types.Message):
    db.del_user(int(message.from_user.id))
    db_main.update_counter(message.from_user.id, 'end')
    await message.answer(mes_santa.end)


inline_btn_1 = types.InlineKeyboardButton('Я отправил!', callback_data='sent_btn')
inline_btn_2 = types.InlineKeyboardButton('Я получил!', callback_data='received_btn')
sent_btn = types.InlineKeyboardMarkup().add(inline_btn_1)
received_btn = types.InlineKeyboardMarkup().add(inline_btn_2)


@dp.callback_query_handler(lambda c: c.data == 'sent_btn')
async def process_callback_button1(callback_query: types.CallbackQuery):
    uid = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    db_drawing.change_sent_st(uid)
    await bot.send_message(uid, '🔔 Отправка подарка подтверждена!')
    await bot.send_message(db_drawing.get_slave(uid), '''📬<b> Вам посылка!</b>

Именно это ты скоро услышишь от почтальона, ведь твой Тайный Санта уже отправил подарок!

Нажми кнопку "Я получил!", когда получишь подарок ''', reply_markup=received_btn)


@dp.callback_query_handler(lambda c: c.data == 'received_btn')
async def process_callback_button1(callback_query: types.CallbackQuery):
    uid = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    db_drawing.change_received_st(uid)
    await bot.send_message(uid, '🔔 Получение подарка подтверждено!')
    await bot.send_message(db_drawing.get_master(uid), '🎁 Твой подопечный получил подарок!')

