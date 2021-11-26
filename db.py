"""
Функции для работы с бд
"""

import config
import psycopg2


class Main:
    """
    Основная бд с инфой о подписчиках
    """
    def __init__(self):
        db = psycopg2.connect(config.DB_URI, sslmode='require')
        cursor = db.cursor()
        self.db, self.cursor = db, cursor

        cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, join_date TIMESTAMP, "
                       "messages INTEGER)")
        db.commit()
        db.close()


class Santa:
    """
    Бд с инфой по тайному санте
    """

    def __init__(self):
        db = psycopg2.connect(config.DB_URI, sslmode='require')
        cursor = db.cursor()
        self.db, self.cursor = db, cursor

        cursor.execute("CREATE TABLE IF NOT EXISTS santa(id INTEGER PRIMARY KEY, username TEXT, wishes TEXT, "
                       "address TEXT, on_meeting BOOLEAN)")
        db.commit()
        db.close()
