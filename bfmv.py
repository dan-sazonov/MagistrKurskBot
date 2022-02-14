from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import features
import logger
from dispatcher import dp, bot

# log = logger.get_logger(__name__)


def init():
    pass


class Polling(StatesGroup):
    Start = State()
    Message = State()
    Title = State()
    TitleText = State()
    Target = State()
    Last = State()


@dp.message_handler(commands=['valentine'])
async def step_0(message: types.Message):
    btn_1 = types.InlineKeyboardButton('❤', callback_data='start_btn')
    kb = types.InlineKeyboardMarkup().add(btn_1)
    await message.answer('''Привет! Ты попал в меню "Тайный Валентин"!

Здесь ты можешь отправить письмо или валентинку любому человеку, ведь сегодня – День святого Валентина – нужно делиться своими чувствами в такие непростые времена 💖

Нажми кнопку "❤", чтобы начать''', reply_markup=kb)
    print(f'{message.from_user.id} start the valentine')


@dp.callback_query_handler(lambda c: c.data == 'start_btn')
async def step_1(callback_query: types.CallbackQuery):
    btn_1 = types.InlineKeyboardButton('💌 Письмо', callback_data='letter')
    btn_2 = types.InlineKeyboardButton('💓 Валентинку', callback_data='sticker')
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
    await bot.send_message(uid, '''Здорово! Отправь сюда стикер, который ты хочешь сделать валентинкой. Ты можешь выбрать его из <a href="t.me/addstickers/love_you_tg_by_fStikBot">стикерпака</a>, собранного нашей командой.''', disable_web_page_preview=True)
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
    await message.answer('''<b>Теперь давай решим, кому ты отправишь послание.</b>

Чтобы оно точно дошло до адресата, нужно отправить ID пользователя.

Вот что нужно сделать:

1. Перейди в диалог с ботом @username_to_id_bot
2. Найди любое сообщение от человека, которому ты хочешь отправить своё послание
3. Перешли это сообщение боту
4. Бот выдаст тебе набор цифр – это тот самый ID, который тебе нужен
5. Скопируй ID и отправь его нашему боту
6. Готово, получатель найден!

Если у тебя нет сообщения от нужного человека, то тогда введи боту @username_to_id_bot его имя и фамилию. Также можешь найти имя пользователя (его можно найти, зайдя в меню контакта, оно будет под значком @)''', reply_markup=types.ReplyKeyboardRemove())
    await Polling.TitleText.set()


@dp.message_handler(state=Polling.TitleText)
async def step_6(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(target=answer)
    await message.answer('Ищем подходящих людей...')

    if answer.isdigit():
        send_to = [int(answer)]
        await state.update_data(send_to=send_to)
        await message.answer(f'''<b>Вот кого нам удалось найти.</b>
        
Если ID человека указан верно, отправь боту цифру <code>1</code>.

Если ты ошибся, или хочешь запустить заново, отправь <code>0</code>, а потом снова вызови команду /valentine

<b>1.</b> {send_to}''')
    else:
        tmp = []
        out = features.find_users(answer)
        await state.update_data(send_to=out)
        for i in range(len(out)):
            tmp.append(f'<b>{i+1}.</b> {"@"+out[i][1] if out[i][1] else ""} <i>({out[i][2].title() if out[i][2] else ""})</i>')
        await message.answer('''<b>Вот кого нам удалось найти.</b>
        
Если ID человека указан верно, отправь боту цифру <code>1</code>.
     
Если ты ошибся, или хочешь запустить заново, отправь <code>0</code>, а потом снова вызови команду /valentine

''' + '\n'.join(tmp))
    await Polling.Target.set()


@dp.message_handler(state=Polling.Target)
async def step_7(message: types.Message, state: FSMContext):
    i = int(message.text) - 1
    if i == -1:
        await state.finish()
        print(f'{message.from_user.id} stop the poll after name search')
        return

    data = await state.get_data()
    print(data)
    out = data.get('send_to')
    if len(out) > 1:
        await state.update_data(slave_id=out[i][0])
        pre = f'''<b>А теперь давай проверим.</b>

Получатель: {"@"+out[i][1] if out[i][1] else ""} <i>({out[i][2].title() if out[i][2] else ""})</i>
{'Стикер' if data.get('type')=='sticker' else 'Текст сообщения'}: <i>{'см. выше' if data.get('type')=='sticker' else data.get('message')}</i>
Подпись: <i>{'нет' if not data.get('title') else data.get('title_text')}</i>'''
    else:
        await state.update_data(slave_id=out[0])
        pre = f'''<b>А теперь давай проверим.</b>

Получатель: <i>{out[0]}</i>
{'Стикер' if data.get('type') == 'sticker' else 'Текст сообщения'}: <i>{'см. выше' if data.get('type') == 'sticker' else data.get('message')}</i>
Подпись: <i>{'нет' if not data.get('title') else data.get('title_text')}</i>'''

    await message.answer(pre)
    btn_1 = types.InlineKeyboardButton('🚀', callback_data='send')
    btn_2 = types.InlineKeyboardButton('🚧', callback_data='abort')
    kb = types.InlineKeyboardMarkup().add(btn_1).add(btn_2)

    await message.answer('''Нажми кнопку "🚀", чтобы отправить сообщение

Нажми кнопку "🚧", чтобы внести изменения''', reply_markup=kb)
    await Polling.Last.set()


@dp.callback_query_handler(lambda c: c.data == 'abort', state=Polling.Last)
async def step_8(callback_query: types.CallbackQuery, state: FSMContext):
    uid = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(uid, '''Что-то пошло не так, данные не получается отредактировать😐

Отправь команду /valentine снова, это точно сработает!''')
    print(f'{uid} stop the poll after date checking')
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'send', state=Polling.Last)
async def step_8(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    uid = callback_query.from_user.id
    title_text = data.get('title_text')
    send_to = data.get('slave_id')

    await bot.answer_callback_query(callback_query.id)

    try:
        if data.get('type') == 'letter':
            await bot.send_message(send_to, f'''<b>Привет! Это бот канала "КРОМО "Магистр".</b>

Даже если ты не слышал о нас, не пугайся. Это не спам-рассылка!

Сегодня, в День святого Валентина, мы проводим необычный флешмоб. Люди пишут нам добрые пожелания для своих друзей, родных и близких, а мы передаём их вот таким необычным способом.

Ты стал адресатом такого сообщения!

Вот что тебе прислали:

<i>{data.get('message')}</i>
''')
            if data.get('title'):
                await bot.send_message(send_to, f'''Более того, мы даже можем сказать тебе, кто это отправил. Это <i>{title_text}</i>! Скорее пожелай ему(ей) тоже чего-то очень светлого и хорошего, это всегда приятно!''')
            else:
                await bot.send_message(send_to, f'''Отправитель не захотел разглашать тебе своего имени. Но ты можешь сам догадаться, кто это мог быть, и написать этому человеку лично, чтобы поблагодарить его и пожелать всего самого сокровенного!''')

        if data.get('type') == 'sticker':
            await bot.send_message(send_to, f'''<b>Привет! Это бот канала "КРОМО "Магистр".</b>

Даже если ты не слышал о нас, не пугайся. Это не спам-рассылка!

Сегодня, в День святого Валентина, мы проводим необычный флешмоб. Люди пишут нам добрые пожелания для своих друзей, родных и близких, а мы передаём их вот таким необычным способом.

Ты стал адресатом такого сообщения!

Вот что тебе прислали:''')
            await bot.send_sticker(send_to, rf'{data.get("message")}')
            if data.get('title'):
                await bot.send_message(send_to, f'''Более того, мы даже можем сказать тебе, кто это отправил. Это <i>{title_text}</i>! Скорее пожелай ему(ей) тоже чего-то очень светлого и хорошего, это всегда приятно!''')
            else:
                await bot.send_message(send_to, f'''Отправитель не захотел разглашать тебе своего имени. Но ты можешь сам догадаться, кто это мог быть, и написать этому человеку лично, чтобы поблагодарить его и пожелать всего самого сокровенного!''')
        print(f'Send data from {uid} to {send_to}')
        await bot.send_message(uid, 'Отлично! Тайный Валентин уже отправил твоё послание :)')
    except Exception as exc:
        print(exc,send_to)
        print('Fail to send')
        await bot.send_message(uid, '''О нет, какая жалость! Получатель твоего прекрасного послания, к сожалению, запретил ботам писать ему сообщения. Из-за этого Тайный Валентин не может передать ему то, что ты отправил.

Не расстраивайся! Ты можешь сказать эти слова тому человеку сам. Ему (или ей) точно будет приятно!''')

    await state.finish()
