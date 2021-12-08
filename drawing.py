"""
Буду предельно прямолинеен: это самый ужасный код, который я сотворил за последнее время. Я вообще не понимаю, что и
зачем здесь происходит. Но если учесть, что он написан спустя 3 часа после дэдлайна и нужен лишь для того, чтобы
автоматизировать ручную работу, переписывать его я смысла не вижу
"""


import random

from db import Santa, Drawing
from dispatcher import dp, bot, storage
from messages import Messages
from aiogram import types

db = Santa()
db_drawing = Drawing()


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


def get_mes_text(slave_id, on_meeting):
    return 'тестовое сообщение мастеру'


test_pairs = [(69, 420, 1), (420, 69, 1)]


def sent_alerts(pairs: list[tuple[int, int, bool]]) -> None:
    if input('ты ебанулся? ') != 'yes':
        pairs = test_pairs

    async def mailing(message: types.Message):
        for pair in pairs:
            await bot.send_message(chat_id=pair[0], text=get_mes_text(pair[1], pair[2]))


if __name__ == "__main__":
    pairs_of_players = get_pairs()
    add_pairs(pairs_of_players)
