import aiogram.utils.exceptions as exc
from aiogram.bot.bot import Bot
import asyncio
import os
import psycopg2

full_names = dict()
users_id = []

##############
# КОНФИГ:
API_TOKEN = os.getenv('BOT_TOKEN')
if not API_TOKEN:
    print('токена нет')
    exit(-1)

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print('урла бд нет')
    exit(-1)
##############


##############
# БД
try:
    db = psycopg2.connect(DATABASE_URL, sslmode='require')
except Exception:
    db = None
    print('урла бд нет')
    exit(-1)

cursor = db.cursor()

# тащим все айдишники из бд:
cursor.execute("SELECT id from users")
for i in cursor.fetchall():
    users_id.append(i[0])

# создаем БД:
cursor.execute("CREATE TABLE IF NOT EXISTS users(id BIGINT PRIMARY KEY, username TEXT, first_name TEXT, "
               "last_name TEXT, full_name TEXT, join_date TIMESTAMP, messages INTEGER)")

cursor.execute("CREATE TABLE IF NOT EXISTS messages(id BIGINT PRIMARY KEY, songs_ INTEGER, contacts_ INTEGER, "
               "howto_ INTEGER, team_ INTEGER, memes_ INTEGER, credits_ INTEGER, help_ INTEGER, start_ INTEGER,"
               "stop_ INTEGER, santa_ INTEGER, end_ INTEGER)")
db.commit()
##############


async def get_tg_names():
    b = Bot(token=API_TOKEN)
    for j in users_id:
        try:
            p = await b.get_chat_member(chat_id=-1001761177569, user_id=j)
        except exc.BadRequest:
            print('fail', j)
            continue
        full_names[p.user.id] = tuple(p.user.full_name.split())
    return


loop = asyncio.get_event_loop()
loop.run_until_complete(get_tg_names())
loop.close()

print(users_id)
print(full_names)
