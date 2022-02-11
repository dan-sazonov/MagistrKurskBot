import logging
import os

_log_format = '%(asctime)s [%(levelname)s] - %(name)s(%(filename)s, %(lineno)d): %(message)s'


def _safe_mkfile(path: str) -> None:
    if not os.path.exists('./logs'):
        os.mkdir('./logs')
    if not os.path.exists(f'./logs/{path}'):
        open(f'./logs/{path}', 'w+').close()


def set_basic_logger():
    _safe_mkfile('main.log')
    logging.basicConfig(level=logging.INFO, filename='./logs/main.log', filemode='w+', format=_log_format)


def get_file_handler():
    _safe_mkfile('warnings.log')
    file_handler = logging.FileHandler('./logs/warnings.log')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger


def get_updates_logger():
    file_handler = logging.FileHandler('./logs/updates.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))

    logger = logging.getLogger('get_updates')
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    return logger
