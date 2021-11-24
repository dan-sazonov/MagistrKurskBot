"""
Основной процесс бота
Все функции и настройки лучше вынести в отдельные файлы.
"""

from aiogram import executor

from dispatcher import dp

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
