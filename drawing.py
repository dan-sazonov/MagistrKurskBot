"""
Буду предельно прямолинеен: это самый ужасный код, который я сотворил за последнее время. Я вообще не понимаю, что и
зачем здесь происходит. Но если учесть, что он написан спустя 3 часа после дэдлайна и нужен лишь для того, чтобы
автоматизировать ручную работу, переписывать его я смысла не вижу
"""

import random
import asyncio
import santa

from aiogram import types
from db import Santa, Drawing, Polling
from dispatcher import bot

db = Santa()
db_drawing = Drawing()
db_polling = Polling()


def get_pairs() -> list[tuple[int, int, bool]]:
    """
    Возвращает список кортежей с парами санта - подопечный и флагом присутствия на встрече
    Зачем нам здесь нужен флаг - в душе не чаю, но к трем утра я уже потерял способность к рассудку

    :return: [(санта, подопечный, on_meeting), ]
    """
    players_on_meeting, players_out_meeting = [], []
    pairs = []
    on_meeting_flag = False

    for player in db.get_players():
        # можно обойтись только одним циклом, но во-первых и так сойдет, а во-вторых, нужно захардкодить рандомизацию
        if player[1]:
            players_on_meeting.append(player[0])
        else:
            players_out_meeting.append(player[0])

    for players in (players_out_meeting, players_on_meeting):
        random.shuffle(players)
        pairs.append((players[-1], players[0], on_meeting_flag))

        for i in range(len(players) - 1):
            pairs.append((players[i], players[i + 1], on_meeting_flag))
        on_meeting_flag = True

    return pairs


def add_pairs(pairs: list[tuple[int, int, bool]]) -> None:
    """
    Добавляет в бд drawing пары участников
    ЗАЧЕМ Я СОЗДАЛ ЕЩЕ ОДНУ БД?!?!

    :param pairs: [(master, slave, on_meeting),]
    :return: None
    """
    counter = 0

    for pair in pairs:
        db_drawing.add_pair(pair)
        counter += 1
    print(f'INFO: {counter} pairs were added to the database')


def get_mes_text(slave_id: int, on_meeting: bool) -> str:
    """
    Возвращает оформленный текст сообщения с подставленными данными слэйва

    :param slave_id: айдишник слэйва, по которому дергаем инфу
    :param on_meeting: будет ли слэйв на встрече
    :return: текст
    """
    data = db.get_info(slave_id)

    txt_out = f'''<b>Привет, дорогой друг!</b> Мы произвели жеребьёвку участников игры "Тайный Санта "Магистра". Теперь мы знаем, кто и кому будет делать подарок. Спешим рассказать и тебе!

Вот как ты можешь найти человека, которому ты делаешь подарок.

<b>ФИО:</b> <i>{data[0]}</i>
<b>Почтовый адрес:</b> <i>{data[1]}</i>
<b>Приедет ли на общелагерную встречу:</b> нет. Свой подарок ты можешь отправить по почте.

<b>Пожелания по подарку:</b> <i>"{data[2]}"</i>

<i>После того, как ты отправишь подарок, нажми кнопку "Я отправил!" под этим сообщением.</i>'''
    txt_on = f'''<b>Привет, дорогой друг!</b> Мы произвели жеребьёвку участников игры "Тайный Санта "Магистра". Теперь мы знаем, кто и кому будет делать подарок. Спешим рассказать и тебе!

Вот как ты можешь найти человека, которому ты делаешь подарок.

<b>ФИО:</b> <i>{data[0]}</i>
<b>Почтовый адрес:</b> <i>{data[1]}</i>
<b>Приедет ли на общелагерную встречу:</b> Да!

<b>Пожелания по подарку:</b> <i>"{data[2]}"</i>
Свой подарок ты можешь как отдать лично на встрече, так и отправить его по почте.

<i>После того, как ты отправишь подарок, нажми кнопку "Я отправил!" под этим сообщением.</i>'''

    return txt_on if on_meeting else txt_out


async def sent_alerts(pairs: list[tuple[int, int, bool]]) -> None:
    """
    Рассылает юзерам сообщение с инфой про их слэйва

    :param pairs: [(санта, подопечный, on_meeting), ]
    :return: None
    """
    for pair in pairs:
        await bot.send_message(chat_id=pair[0], text=get_mes_text(pair[1], pair[2]), reply_markup=santa.sent_btn)
        await bot.close()  # жуткий костыль, но без него все сыпется. А так только варнинг летит
        await asyncio.sleep(30)


async def sent_questions() -> None:
    """
    Рассылает юзерам сообщение с началом повторного опроса

    :return: None
    """

    inline_btn_1 = types.InlineKeyboardButton('Поехали!', callback_data='start_pol')
    start_pol_kb = types.InlineKeyboardMarkup().add(inline_btn_1)

    users = [(385056286, 'dan')]
    # users = db.get_users()
    for user in users:
        await bot.send_message(chat_id=user[0], text='''Привет, дорогой друг! Это команда телеграм-канала "КРОМО "Магистр".

Мы знаем, что ты принимал участие в игре "Тайный Санта "Магистра", и хотим сделать ее лучше! Для этого ответь, пожалуйста, на несколько вопросов.''', reply_markup=start_pol_kb)
        print(f'sent to {user[0]}')
        await bot.close()  # жуткий костыль, но без него все сыпется. А так только варнинг летит
        await asyncio.sleep(30)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sent_questions())
    loop.close()
