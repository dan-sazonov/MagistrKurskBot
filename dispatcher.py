"""
Создает и настраивает бота
Все, что связано с обработкой сообщений, должно быть помещено в `handlers.py`.
"""
import logging
import config
import aiogram
import messages

from filters import IsOwnerFilter, IsAdminFilter, MemberCanRestrictFilter

mes_songs = messages.Messages.Songs()
mes_contacts = messages.Messages.Contacts()

# Configure logging
logging.basicConfig(level=logging.INFO)

# кастомные костыльные логи
if config.ENABLE_ECHO:
    print('INFO: echo mode enable')

# init
TOKEN = config.API_TOKEN
bot = aiogram.Bot(token=TOKEN, parse_mode="HTML")
dp = aiogram.Dispatcher(bot)

# activate filters
dp.filters_factory.bind(IsOwnerFilter)
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(MemberCanRestrictFilter)

# создаем клавы с кнопками
# для /songs:
songs_kb = aiogram.types.InlineKeyboardMarkup()
songs_kb.add(aiogram.types.InlineKeyboardButton(mes_songs.web_text, url=mes_songs.web_link))
songs_kb.add(aiogram.types.InlineKeyboardButton(mes_songs.app_text, url=mes_songs.app_link))
# для /contacts
contacts_kb = aiogram.types.InlineKeyboardMarkup()
contacts_kb.add(aiogram.types.InlineKeyboardButton(mes_contacts.vk_text, url=mes_contacts.vk_link))
contacts_kb.add(aiogram.types.InlineKeyboardButton(mes_contacts.inst_text, url=mes_contacts.inst_link))
contacts_kb.add(aiogram.types.InlineKeyboardButton(mes_contacts.web_text, url=mes_contacts.web_link))
contacts_kb.add(aiogram.types.InlineKeyboardButton(mes_contacts.tt_text, url=mes_contacts.tt_link))
contacts_kb.add(aiogram.types.InlineKeyboardButton(mes_contacts.yt_text, url=mes_contacts.yt_link))
contacts_kb.add(aiogram.types.InlineKeyboardButton(mes_contacts.tg_text, url=mes_contacts.tg_link))

