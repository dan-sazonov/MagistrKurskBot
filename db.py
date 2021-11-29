"""
Функции для работы с бд
"""

import config
import psycopg2
import datetime


class Main:
    """
    Основная бд с инфой о подписчиках
    """

    def __init__(self):
        db = psycopg2.connect(config.DATABASE_URL, sslmode='require')
        cursor = db.cursor()
        self.db, self.cursor = db, cursor

        cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, join_date TIMESTAMP, "
                       "messages INTEGER)")
        db.commit()

    def add_user(self, user_id: int, username: str) -> None:
        """
        Добавляет юзера в бд, если он еще не добавлен

        :param user_id: telegram id юзера
        :param username: имя юзера
        :return: None
        """
        self.cursor.execute(f"SELECT id FROM users WHERE id = {user_id}")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO users(id, username, join_date, messages) VALUES (%s, %s, %s, %s)",
                                (user_id, username, datetime.datetime.now(), 0))
        self.db.commit()

    def del_user(self, user_id: int) -> None:
        """
        Удаляет юзера из бд, если он еще там

        :param user_id: telegram id юзера
        :return: None
        """
        self.cursor.execute(f"SELECT id FROM users WHERE id = {user_id}")
        if self.cursor.fetchone():
            self.cursor.execute(f"DELETE FROM users WHERE id = {user_id}")

        self.db.commit()

    def update_counter(self, user_id: int, count=1) -> None:
        """
        Изменяет количество отправленных сообщениий

        :param user_id: telegram id юзера
        :param count: инкремент, по дефолту 1
        :return: None
        """
        self.cursor.execute(f"UPDATE users SET messages = messages + {count} WHERE id = {user_id}")
        self.db.commit()


class Santa:
    """
    Бд с инфой по тайному санте
    """

    # Да, я слышал про DRY. Интересно, почему код должен быть сухим?

    def __init__(self):
        db = psycopg2.connect(config.DATABASE_URL, sslmode='require')
        cursor = db.cursor()
        self.db, self.cursor = db, cursor

        cursor.execute("CREATE TABLE IF NOT EXISTS santa(id INTEGER PRIMARY KEY, wishes TEXT, address TEXT, name TEXT,"
                       "on_meeting BOOLEAN, gift_sent BOOLEAN, gift_received BOOLEAN)")
        db.commit()

    def add_user(self, user_id: int, data: dict) -> None:
        """
        Добавляет участника в бд, если он еще не добавлен

        :param user_id: telegram id юзера
        :param data: словарь со значениями для стобцов БД
        :return: None
        """
        self.cursor.execute(f"SELECT id FROM santa WHERE id = {user_id}")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO santa(id, wishes, address, name, on_meeting, gift_sent, gift_received) "
                                "VALUES (%s, %s, %s, %s, %s, FALSE, FALSE)", (user_id, data['wishes'], data['address'],
                                                                          data['name'], data['on_meeting']))
        self.db.commit()

    def del_user(self, user_id: int) -> None:
        """
        Удаляет участника из бд, если он еще там

        :param user_id: telegram id юзера
        :return: None
        """
        self.cursor.execute(f"SELECT id FROM santa WHERE id = {user_id}")
        if self.cursor.fetchone():
            self.cursor.execute(f"DELETE FROM santa WHERE id = {user_id}")

        self.db.commit()
