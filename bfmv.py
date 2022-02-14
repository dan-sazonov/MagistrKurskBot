from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import features
from dispatcher import dp, bot


def init():
    pass


class Polling(StatesGroup):
    Start = State()
    Message = State()
    Title = State()
    TitleText = State()
    Target = State()


@dp.message_handler(commands=['valentine'])
async def step_0(message: types.Message):
    btn_1 = types.InlineKeyboardButton('U+2764', callback_data='start_btn')
    kb = types.InlineKeyboardMarkup().add(btn_1)
    await message.answer('''Привет! Ты попал в меню "Тайный Валентин"!

Здесь ты можешь отправить письмо или валентинку любому человеку, ведь сегодня – День святого Валентина – нужно делиться своими чувствами в такие непростые времена U+1F496

Нажми кнопку "U+2764", чтобы начать''', reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data == 'start_btn')
async def step_1(callback_query: types.CallbackQuery):
    btn_1 = types.InlineKeyboardButton('письмо', callback_data='letter')
    btn_2 = types.InlineKeyboardButton('стикер', callback_data='sticker')
    kb = types.InlineKeyboardMarkup().add(btn_1).add(btn_2)

    uid = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(uid, '''Отлично, приступим!
Что ты хочешь отправить?''', reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data == 'letter', state=None)
async def step_2_1(callback_query: types.CallbackQuery, state: FSMContext):
    uid = callback_query.from_user.id
    await state.update_data(type='letter')
    await state.update_data(uid=uid)

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(uid,
                           'Прекрасный выбор! Напиши в ответном сообщении то, что хотел бы сказать получателю письма')
    await Polling.Start.set()


@dp.callback_query_handler(lambda c: c.data == 'sticker', state=None)
async def step_2_2(callback_query: types.CallbackQuery, state: FSMContext):
    uid = callback_query.from_user.id
    await state.update_data(type='sticker')
    await state.update_data(uid=uid)

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(uid, '''Здорово! Отправь сюда стикер, который ты хочешь сделать валентинкой''')
    await Polling.Start.set()


@dp.message_handler(state=Polling.Start, content_types='sticker')
async def step_3_1(message: types.Message, state: FSMContext):
    answer = message.sticker.file_id
    await state.update_data(message=answer)

    btn_1 = types.InlineKeyboardButton('Да!', callback_data='title_true')
    btn_2 = types.InlineKeyboardButton('Нет', callback_data='title_false')
    kb = types.InlineKeyboardMarkup().add(btn_1).add(btn_2)

    await message.answer('Хочешь подписать свою валентинку?', reply_markup=kb)
    await Polling.Message.set()


@dp.message_handler(state=Polling.Start, content_types='text')
async def step_3_2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(message=answer)

    btn_1 = types.InlineKeyboardButton('Да!', callback_data='title_true')
    btn_2 = types.InlineKeyboardButton('Нет', callback_data='title_false')
    kb = types.InlineKeyboardMarkup().add(btn_1).add(btn_2)

    await message.answer('Хочешь подписать своё письмо?', reply_markup=kb)
    await Polling.Message.set()


@dp.callback_query_handler(lambda c: c.data == 'title_true', state=Polling.Message)
async def step_4_1(callback_query: types.CallbackQuery, state: FSMContext):
    uid = callback_query.from_user.id
    await state.update_data(title=True)

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(uid, '''Тогда придумай себе уникальную подпись и отправь её в ответном сообщении!''')
    await Polling.Title.set()


@dp.callback_query_handler(lambda c: c.data == 'title_false', state=Polling.Message)
async def step_4_2(callback_query: types.CallbackQuery, state: FSMContext):
    uid = callback_query.from_user.id
    await state.update_data(title=False)

    mes_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = types.KeyboardButton('Идем дальше!')
    mes_kb.add(btn_1)

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(uid, '''Окей, нет проблем!''', reply_markup=mes_kb)
    await Polling.Title.set()


@dp.message_handler(state=Polling.Title)
async def step_5(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(title_text=answer)
    await message.answer('Теперь давай решим, кому ты отправишь послание. Можешь написать его настоящее имя (желательно с фамилией), имя аккаунта в Телеграме или указать ссылку на его аккаунт (она должна начинаться с t.me или @)', reply_markup=types.ReplyKeyboardRemove())
    await Polling.TitleText.set()


@dp.message_handler(state=Polling.TitleText)
async def step_6(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(target=answer)
    await message.answer('Ищем подходящих людей...')

    if answer.isdigit():
        send_to = [int(answer)]
        await state.update_data(send_to=send_to)
        await message.answer(f'''Вот кого нам удалось найти. Выбери цифру, которая соответствует нужному тебе человеку, и отправь её в ответ:

<b>1.</b> {send_to}''')
    else:
        tmp = []
        out = features.find_users(answer)
        await state.update_data(send_to=out)
        for i in range(len(out)):
            tmp.append(f'<b>{i+1}.</b> {"@"+out[i][1] if out[i][1] else ""} <i>({out[i][2].title() if out[i][2] else ""})</i>')
        await message.answer('Вот кого нам удалось найти. Выбери цифру, которая соответствует нужному тебе человеку, и отправь её в ответ:\n\n' + '\n'.join(tmp))
    await Polling.Target.set()


@dp.message_handler(state=Polling.Target)
async def step_7(message: types.Message, state: FSMContext):
    i = int(message.text) - 1
    data = await state.get_data()
    print(data)
    out = data.get('send_to')
    pre = f'''<b>А теперь давай проверим.</b>

Получатель: {"@"+out[i][1] if out[i][1] else ""} <i>({out[i][2].title() if out[i][2] else ""})</i>
{'Стикер' if data.get('type')=='sticker' else 'Текст сообщения'}: <i>{'см. выше' if data.get('type')=='sticker' else data.get('message')}</i>
Подпись: <i>{'нет' if not data.get('title') else data.get('title_text')}</i>'''

    await message.answer(pre)
    btn_1 = types.InlineKeyboardButton('🚀', callback_data='send')
    btn_2 = types.InlineKeyboardButton('🚧', callback_data='abort')
    kb = types.InlineKeyboardMarkup().add(btn_1).add(btn_2)

    await message.answer('''Нажми кнопку "🚀", чтобы отправить сообщение
    
Нажми кнопку "🚧", чтобы внести изменения''', reply_markup=kb)
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'abort')
async def step_8(callback_query: types.CallbackQuery):
    uid = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(uid, '''Что-то пошло не так, данные не получается отредактировать😐

Отправь команду /valentine снова, это точно сработает!''')