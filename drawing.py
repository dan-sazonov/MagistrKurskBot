from db import Santa
import random

db = Santa()


def get_pairs() -> list[tuple[int, int]]:
    """
    Возвращает список кортежей с парами санта - подопечный

    :return: [(санта, подопечный), ]
    """

    players = db.get_players()
    # players = [1, 2, 3, 4, 5]  # для дебага
    random.shuffle(players)

    pairs = [(players[-1], players[0])]
    for i in range(len(players)-1):
        pairs.append((players[i], players[i+1]))

    return pairs

