"""
Основной процесс бота
Все функции и настройки лучше вынести в отдельные файлы.
"""
from aiogram import executor

import exceptions
import handlers
import logger
from dispatcher import dp

log = logger.get_logger(__name__)
log.info('Run main.py')

if __name__ == "__main__":
    log.info('Main process has been started')
    exceptions.AiogramExc()
    executor.start_polling(dp, skip_updates=True, on_startup=handlers.on_startup, on_shutdown=handlers.on_shutdown)
    log.info('Main process has been finished')
