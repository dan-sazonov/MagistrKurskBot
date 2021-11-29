from dispatcher import dp, bot
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from messages import Messages


def init():
    # костыль, чтобы импорт в handlers.py не был пустым
    pass


messages = Messages()
mes_santa = Messages.Santa()


class Poll(StatesGroup):
    Wishes = State()
    OnMeeting = State()
    Address = State()


@dp.message_handler(Command("santa"), state=None)
async def start_polling(message: types.Message):
    await message.answer(mes_santa.on_start_1)
    await message.answer(mes_santa.ask_wishes)

    await Poll.Wishes.set()


@dp.message_handler(state=Poll.Wishes)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(wishes=answer)

    mes_kb = types.ReplyKeyboardMarkup(row_width=2)
    inline_btn_3 = types.KeyboardButton('Да!')
    inline_btn_4 = types.KeyboardButton('Нет')
    mes_kb.row(inline_btn_3, inline_btn_4)

    await message.answer(mes_santa.ask_meeting, reply_markup=mes_kb)
    await Poll.OnMeeting.set()


@dp.message_handler(state=Poll.OnMeeting)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(on_meeting=answer)

    await message.answer(mes_santa.ask_address)
    await Poll.next()


@dp.message_handler(state=Poll.Address)
async def answer_q3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    form = {'wishes': data.get("wishes"), 'on_meeting': data.get("on_meeting"), 'address': message.text}

    print(form)

    await message.answer(mes_santa.on_end)
    await state.finish()
