"""
Функции для работы с бд
"""

import datetime
import random
from typing import Tuple

import psycopg2

import config
import logger

log = logger.get_logger(__name__)


class Main:
    """
    Основная бд с инфой о подписчиках
    """

    def __init__(self):
        """
        Проверяет коннект к бд, ловит ошибки. Создает объекты бд и курсора. Создает, если еще не созданы таблицы бд
        """
        try:
            log.info('Trying to connect to the database')
            db = psycopg2.connect(config.DATABASE_URL, sslmode='require')
        except TypeError or psycopg2.ProgrammingError:
            log.warning('Failed connection to the database or incorrect URL')
            return
        cursor = db.cursor()
        self.db, self.cursor = db, cursor
        self.last_meme = -1

        cursor.execute("CREATE TABLE IF NOT EXISTS users(id BIGINT PRIMARY KEY, username TEXT, first_name TEXT, "
                       "last_name TEXT, full_name TEXT, join_date TIMESTAMP, messages INTEGER)")

        cursor.execute("CREATE TABLE IF NOT EXISTS messages(id BIGINT PRIMARY KEY, songs_ INTEGER, contacts_ INTEGER, "
                       "howto_ INTEGER, team_ INTEGER, memes_ INTEGER, credits_ INTEGER, help_ INTEGER, start_ INTEGER,"
                       "stop_ INTEGER, santa_ INTEGER, end_ INTEGER, valentine_ INTEGER)")
        db.commit()
        log.info('Successful connection to the database')

    def add_counter(self, user_id: int) -> None:
        """
        Добавляет юзера в бд - счетчик сообщений, если он еще не добавлен

        :param user_id: telegram id юзера
        :return: None
        """
        self.cursor.execute(f"SELECT id FROM messages WHERE id = {user_id}")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO messages(id, songs_, contacts_, howto_, team_, memes_, credits_, help_,"
                                "start_, stop_, santa_, end_, valentine_) "
                                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (user_id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
            log.info(f'The `{user_id}` has been added to the `messages` table')
        self.db.commit()

    def add_user(self, user_id: int, username: str, tg_name: Tuple[str, str], full_name='') -> None:
        """
        Добавляет юзера в бд, если он еще не добавлен

        :param tg_name: кортеж с укуазаннами именами юзера в телеге: (first_name, last_name)
        :param full_name: полное ФИО юзера, опционально можно передать
        :param user_id: telegram id юзера
        :param username: имя юзера
        :return: None
        """
        self.cursor.execute(f"SELECT id FROM users WHERE id = {user_id}")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO users(id, username, first_name, last_name, full_name, join_date, messages)"
                                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                (user_id, username, *tg_name, full_name, datetime.datetime.now(), 0))
            log.info(f'The `{user_id}` has been added to the `users` table')
        self.db.commit()
        self.add_counter(user_id)

    def del_user(self, user_id: int) -> None:
        """
        Удаляет юзера из всех бд, если он еще там

        :param user_id: telegram id юзера
        :return: None
        """
        for database in ['users']:
            self.cursor.execute(f"SELECT id FROM {database} WHERE id = {user_id}")
            if self.cursor.fetchone():
                self.cursor.execute(f"DELETE FROM {database} WHERE id = {user_id}")
                log.info(f'The `{user_id}` has been deleted from the `{database}` table')
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

        if command in {'songs', 'contacts', 'howto', 'team', 'memes', 'credits', 'help', 'start', 'stop',
                       'santa', 'end'}:
            self.cursor.execute(f"UPDATE messages SET {command + '_'} = {command + '_'} + {count} WHERE id = {user_id}")
            log.info(f'The value of messages.`{command}` has been increased for `{user_id}` by {count}')

        self.cursor.execute(f"UPDATE users SET messages = messages + {count} WHERE id = {user_id}")
        log.info(f'The value of users.messages has been increased for `{user_id}` by {count}')
        self.db.commit()

    def get_random_meme(self):
        while True:
            meme_id = random.randint(0, 12)
            if meme_id != self.last_meme:
                self.last_meme = meme_id
                break

        self.cursor.execute(f"SELECT file_id FROM memes WHERE id = {meme_id}")
        meme_hash = self.cursor.fetchone()

        if not meme_hash:
            log.warning(f'Fail to get meme by id {meme_id}')
            return ''
        return meme_hash[0]
