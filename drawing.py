from db import Santa, Drawing
import random

db = Santa()
db_drawing = Drawing()


def get_pairs() -> list[tuple[int, int, bool]]:
    """
    Возвращает список кортежей с парами санта - подопечный и флагом присутствия на встрече

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

    :param pairs: [(master, slave, on_meeting),]
    :return: None
    """

    counter = 0

    for pair in pairs:
        db_drawing.add_pair(pair)
        counter += 1
    print(f'INFO: {counter} pairs were added to the database')


def sent_alerts(pairs: list[tuple[int, int, bool]]) -> None:
    pass


if __name__ == "__main__":
    pairs_of_players = get_pairs()
    add_pairs(pairs_of_players)
