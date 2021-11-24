"""
Тексты всех сообщений
Файл могут редактировать неайтишники, все должно быть антивандально. Все функции по обработке пихаем в `handlers.py`
"""
import config


class Messages:
    """
    Тексты сообщений, отправляемые ботом
    """

    def __init__(self):
        # не лезь, оно сожрет тебя
        self.foo = 'bar'
        self.admin_id = config.ADMIN_CHAT
        self.start_polling = '🔔 Бот запущен'
        self.stop_polling = '🔔 Бот остановлен'

    class Songs:
        def __init__(self):
            self.mes_text = 'fuck'
            self.web_text = 'bitch'
            self.web_link = 'bitch'
            self.app_text = 'bitch'
            self.app_link = 'bitch'

    class Contacts:
        def __init__(self):
            self.mes_text = 'fuck'
            self.vk_text = 'bitch'
            self.vk_link = 'bitch'
            self.inst_text = 'bitch'
            self.inst_link = 'bitch'
            self.web_text = 'bitch'
            self.web_link = 'bitch'
            self.tt_text = 'bitch'
            self.tt_link = 'bitch'
            self.yt_text = 'bitch'
            self.yt_link = 'bitch'
            self.tg_text = 'bitch'
            self.tg_link = 'bitch'
