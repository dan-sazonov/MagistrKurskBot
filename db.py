"""
Функции для работы с бд
"""

import config
import psycopg2
import datetime

from typing import List, Tuple

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

    def get_players(self) -> List[Tuple[int, bool]]:
        """
        Возвращает список с айдишниками и флагами участия всех участников

        :return: [(id, on_meeting), ]
        """
        players = []
        self.cursor.execute(f"SELECT id, on_meeting FROM santa")
        for player in self.cursor.fetchall():
            players.append(player)
        return players

    def get_info(self, user_id: int) -> tuple:
        """
        Возвращает основную инфу про участника. Переносы строк меняются на пробелы

        :param user_id: айдишник участника
        :return: (фио, адрес, пожелания)
        """
        self.cursor.execute(f"SELECT id FROM santa WHERE id = {user_id}")
        if not self.cursor.fetchone():
            return 'Ошибка!', 'Ошибка!', 'Ошибка!'

        self.cursor.execute(f"SELECT name, address, wishes FROM santa WHERE id = {user_id}")
        return tuple(map(lambda x: x.replace('\n', ' '), self.cursor.fetchall()[0]))

    def get_users(self) -> List[Tuple[int, str]]:
        """
        Возвращает список с айдишниками и флагами участия всех участников

        :return: [(id, on_meeting), ]
        """
        players = []
        self.cursor.execute(f"SELECT id, name FROM santa")
        for player in self.cursor.fetchall():
            players.append(player)
        return players


def get_user_name(uid:int) -> str:
    """
    Возвращает фио чела из ТС по айдишнику

    :param uid: телеграм-айдишник чела
    :return: фио чела
    """
    return Santa().get_info(uid)[0]


class Drawing:
    """
    БД с инфой по жеребьевке
    """

    def __init__(self):
        db = psycopg2.connect(config.DATABASE_URL, sslmode='require')
        cursor = db.cursor()
        self.db, self.cursor = db, cursor

        cursor.execute("CREATE TABLE IF NOT EXISTS drawing(master BIGINT PRIMARY KEY, slave BIGINT, "
                       "on_meeting BOOLEAN, gift_sent BOOLEAN, gift_received BOOLEAN)")

        db.commit()

    def add_pair(self, data: Tuple[int, int, bool]) -> None:
        """
        Добавляет в бд пару участников. master - санта, slave - подопечный, on_meeting - будут ли m/s на встрече

        :param data: (master, slave, on_meeting)
        :return: None
        """
        self.cursor.execute(f"SELECT master FROM drawing WHERE master = {data[0]}")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO drawing(master, slave, on_meeting, gift_sent, gift_received) "
                                "VALUES (%s,%s,%s, FALSE, FALSE)", data)

        self.db.commit()

    def change_sent_st(self, user_id: int) -> None:
        """
        Ставит флаг gift_sent выбранного юзера в true

        :param user_id: id юзера
        :return: None
        """
        self.cursor.execute(f"SELECT master FROM drawing WHERE master = {user_id}")
        if not self.cursor.fetchone():
            print(f'ERR: user {user_id} not found in the database')
            return None

        self.cursor.execute(f"UPDATE drawing SET gift_sent = TRUE WHERE master = {user_id}")
        self.db.commit()

    def change_received_st(self, user_id: int) -> None:
        """
        Ставит флаг gift_received выбранного юзера в true

        :param user_id: id юзера
        :return: None
        """
        self.cursor.execute(f"SELECT master FROM drawing WHERE master = {user_id}")
        if not self.cursor.fetchone():
            print(f'ERR: user {user_id} not found in the database')
            return None

        self.cursor.execute(f"UPDATE drawing SET gift_received = TRUE WHERE master = {user_id}")
        self.db.commit()

    def get_slave(self, master_id: int) -> int:
        """
        Возвращает телеграм-айдишник слэйва по айдишнику мастера

        :param master_id: айдишник мастера
        :return: айдишник слэйва
        """
        self.cursor.execute(f"SELECT master FROM drawing WHERE master = {master_id}")
        if not self.cursor.fetchone():
            print(f'ERR: user {master_id} not found in the database')
            return config.ADMIN_CHAT

        self.cursor.execute(f"SELECT slave FROM drawing WHERE master = {master_id}")
        return self.cursor.fetchone()[0]

    def get_master(self, slave_id: int) -> int:
        """
        Возвращает телеграм-айдишник мастера по айдишнику слэйва

        :param slave_id: айдишник слэйва
        :return: айдишник мастера
        """
        self.cursor.execute(f"SELECT master FROM drawing WHERE slave = {slave_id}")
        if not self.cursor.fetchone():
            print(f'ERR: user {slave_id} not found in the database')
            return config.ADMIN_CHAT

        self.cursor.execute(f"SELECT master FROM drawing WHERE slave = {slave_id}")
        return self.cursor.fetchone()[0]


class Polling:
    """
    БД с инфой по повторному опросу
    """

    def __init__(self):
        db = psycopg2.connect(config.DATABASE_URL, sslmode='require')
        cursor = db.cursor()
        self.db, self.cursor = db, cursor

        cursor.execute("CREATE TABLE IF NOT EXISTS polling(master_id BIGINT PRIMARY KEY, master_name TEXT, "
                       "slave_name TEXT, gift_sent INTEGER, gift_received INTEGER)")

        db.commit()

    def add_slave_name(self, master_id: int, name: str) -> None:
        """
        Добавялет в бд пользователя, его имя и имя слэйва

        :param master_id: айдишник мастера
        :param name: имя слэйва
        :return: None
        """
        self.cursor.execute(f"SELECT master_id FROM polling WHERE master_id = {master_id}")
        if not self.cursor.fetchone():
            print(0)
            self.cursor.execute("INSERT INTO polling(master_id, master_name, slave_name, gift_sent, gift_received) "
                                "VALUES (%s,%s,%s, 0, 0)", (master_id, get_user_name(master_id), name))
        self.db.commit()

    def update_data(self, master_id: int, sent_state: int, received_state: int) -> None:
        """
        Задает флаги в бд для конкретного мастера
        1 - почта
        2 - встреча
        0 - никак

        :param master_id: айдишник мастера
        :param sent_state: статус получения
        :param received_state: статус отправки
        :return:
        """
        self.cursor.execute(f"SELECT master_id FROM polling WHERE master_id = {master_id}")
        if not self.cursor.fetchone():
            print(f'ERR: user {master_id} not found in the database')
            return None

        self.cursor.execute(f"UPDATE polling SET gift_sent = {sent_state}, gift_received = {received_state}"
                            f" WHERE master_id = {master_id}")
        self.db.commit()

    def get_masters(self) -> set:
        """
        Возвращает множество айдишников, которые проголосовали в опросе

        :return: set(id:int,)
        """
        players = set()
        self.cursor.execute(f"SELECT master_id FROM polling")
        for player in self.cursor.fetchall():
            players.add(player[0])
        return players


def get_non_voting() -> set:
    """
    Возвращает множество айдишников, которые играли в ТС но не проголосовали в опросе

    :return: set(id:int,)
    """
    return set(i[0] for i in Santa().get_users()) - Polling().get_masters()
