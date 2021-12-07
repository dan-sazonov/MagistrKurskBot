from db import Santa
import random

db = Santa()


def get_pairs():
    players = db.get_players()
