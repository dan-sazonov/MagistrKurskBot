"""
Функции для работы с бд
"""

import datetime

import psycopg2

import config


class Main:
    """
    Основная бд с инфой о подписчиках
    """

    def __init__(self):
        try:
            db = psycopg2.connect(config.DATABASE_URL, sslmode='require')
        except TypeError or psycopg2.ProgrammingError:
            msg = f"Failed connection to the database or incorrect URL"
            print(msg)
            return
        cursor = db.cursor()
        self.db, self.cursor = db, cursor

        cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, join_date TIMESTAMP, "
                       "messages INTEGER)")
        cursor.execute("CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY, songs_ INTEGER, contacts_ INTEGER, "
                       "howto_ INTEGER, team_ INTEGER, memes_ INTEGER, credits_ INTEGER, help_ INTEGER, start_ INTEGER,"
                       "stop_ INTEGER, santa_ INTEGER, end_ INTEGER)")
        db.commit()

    def add_counter(self, user_id: int) -> None:
        """
        Добавляет юзера в бд - счетчик сообщений, если он еще не добавлен

        :param user_id: telegram id юзера
        :return: None
        """
        self.cursor.execute(f"SELECT id FROM messages WHERE id = {user_id}")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO messages(id, songs_, contacts_, howto_, team_, memes_, credits_, help_,"
                                "start_, stop_, santa_, end_) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (user_id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.db.commit()

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
        self.add_counter(user_id)

    def del_user(self, user_id: int) -> None:
        """
        Удаляет юзера из всех бд, если он еще там

        :param user_id: telegram id юзера
        :return: None
        """
        for database in ['users', 'messages', 'santa']:
            self.cursor.execute(f"SELECT id FROM {database} WHERE id = {user_id}")
            if self.cursor.fetchone():
                self.cursor.execute(f"DELETE FROM {database} WHERE id = {user_id}")
            self.db.commit()

    def update_counter(self, user_id: int, command: str, count=1) -> None:
        """
        Изменяет количество отправленных сообщениий

        :param user_id: telegram id юзера
        :param command: название вызванной команды
        :param count: инкремент, по дефолту 1
        :return: None
        """
        self.add_counter(user_id)
        self.cursor.execute(f"UPDATE users SET messages = messages + {count} WHERE id = {user_id}")
        self.cursor.execute(f"UPDATE messages SET {command + '_'} = {command + '_'} + {count} WHERE id = {user_id}")
        self.db.commit()
