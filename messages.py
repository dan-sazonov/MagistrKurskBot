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

        self.not_command = '''Я ничего не понял. Чтобы посмотреть список команд бота, введи /help'''
        self.help = '''<b>Что тебя интересует?</b>
    /memes - получить мем
    /contacts - контакты КРОМО "Магистр"
    /team - педсостав центра
    /howto - как попасть на смену
    /songs - песенник Магистра
    /credits - наша команда
    /stop - остановить бота и удалить данные о себе

🎅 <b>Тайный санта</b>
    /santa - начать участие
    /end - удалить заявку

<i>Бот-помощник канала "КРОМО "Магистр" работает на открытом исходном коде, который размещён на портале "Github". За подробностями отправляйся по <a href="https://github.com/dan-sazonov/MagistrKurskBot">ссылке</a>.</i>'''

        self.subscribe = '''<b>Привет, дорогой друг!</b> Это бот-помощник официального Telegram-канала КРОМО "Магистр".

Что тебя интересует?
    /memes - получить мем
    /contacts - контакты КРОМО "Магистр"
    /team - педсостав центра
    /howto - как попасть на смену
    /songs - песенник Магистра
    /credits - наша команда
    /santa - начать участие в Тайном Санте'''
        self.do_unsubscribe = '''Чтобы отписаться, напишите в этот чат «/stop» или «/unsubscribe»'''

        self.unsubscribe = '''Очень жаль, что ты нас покидаешь! Возвращайся скорее!'''
        self.do_subscribe = '''Для повторной подписки введите «/start» или «/subscribe»'''

    class Songs:
        def __init__(self):
            self.mes_text = '''Песенник - это особый сборник песен, где можно найти самые главные песни, важные для каждого магистровца.

Обычно песенники выдают на память всем участникам смен, но если вы хотите найти любимые песни ещё быстрее, то:'''
            self.mes_kb = (('📌 переходите на сайт', 'http://magistrarium.ru/песенник'),
                           ('📥 скачивайте приложение "Песенник"', 'https://trashbox.ru/topics/148839/pesennik-1.1'))

    class Contacts:
        def __init__(self):
            self.mes_text = 'Подписывайся на все официальные аккаунты нашего центра! Так ты сможешь полностью погрузиться в магистровскую атмосферу и узнавать любые новости из первых рук!'
            self.mes_kb = (('🔔 Группа ВКонтакте', 'https://vk.com/kromomagistr'),
                           ('📸 Аккаунт в Instagram', 'https://instagram.com/magistrkursk'),
                           ('📌 Наш сайт', 'http://magistrarium.ru/'),
                           ('🎵 Аккаунт в TikTok', 'https://vm.tiktok.com/ZSe6pAoSQ/'), ('📺 Магистр ТВ - YouTube',
                                                                                         'https://www.youtube.com/c/%25D0%259C%25D0%25B0%25D0%25B3%25D0%25B8%25D1%2581%25D1%2582%25D1%2580%25D0%25A2%25D0%2592'),
                           ('🔔 Канал в Telegram', 'https://t.me/magistrKursk'))

    class HowTo:
        def __init__(self):
            self.mes_text = '''При составлении списка участников смены приоритет имеют дети, которые стали призерами или победителями:
✅ Всероссийской олимпиады школьников на региональном или всероссийском уровне;
✅ олимпиад, утверждённых перечнем Министерства просвещения Российской Федерации;
✅ других олимпиад и конкурсов регионального и всероссийского уровней.

В этом случае наша команда, скорее всего, самостоятельно пригласит вас в "Магистр" или свяжется через отдел молодёжной политики в вашем городе или районе. Чаще всего их зачисление производится на бюджетной основе.

Вы также можете купить путёвку в наш центр. Для этого свяжитесь с председателем КС КРОМО "Магистр" Лопатко Александром Игоревичем через соцсети "Магистра" или:
📱 по телефону +79102706680
📨 по электронной почте kromo-magistr@mail.ru
💡 лично по адресу 305000, г. Курск, ул. Радищева, 33, оф. 335
💡 по почте 305000, г. Курск, ул. Радищева, 33, каб. 36'''

    class Team:
        def __init__(self):
            self.mes_text = '''ПРЕДСЕДАТЕЛЬ КООРДИНАЦИОННОГО СОВЕТА КРОМО "Магистр"
Лопатко Александр Игоревич

МЕТОДИСТЫ
▪️Бердышев Даниил Игоревич
▪️Климентьева Анна Дмитриевна
▪️Клюева Ксения Ивановна
▪️Ченцов Ярослав Дмитриевич
▪️Ланских Анна Валерьевна

ДИДЖЕИ
▫️Никонов Егор АлексеевичБаранов
▫️Константин Сергеевич

ХУДОЖНИКИ
🔔Дьячкова Елена Михайловна
🔔Алябьева Ирина Михайловна

СТАЖЁРЫ
📍Войтенко Владислав Андреевич
📍Кузьменко Александра Александровна
📍Гулянкова Анастасия Евгеньевна

МАГИСТРЫ
📌Кругликов Кирилл Владимирович
📌Гукова Валерия Викторовна
📌Полянская Диана Сергеевна
📌Алфёров Григорий Александрович
📌Лукина Яна Евгеньевна
📌Кудрявцев Владислав Юрьевич
📌Субботина Ирина Борисовна
📌Новиков Даниил Александрович
📌Хмелевской Даниил Александрович
📌Макарьева Карина Алексеевна
📌Костина Карина Романовна
📌Водолад Дмитрий Владиславович
📌Пашкова Тамара Олеговна
📌Матвеева Татьяна Александровна
📌Матвеев Максим Александрович
📌Овсянников Александр Владимирович
📌Дощечкина Глафира Денисовна
📌Агибалова Кристина Станиславовна
📌Лаптев Даниил Александрович
📌Федосов Даниил Станиславович

Список педагогического состава актуален на лето и осень 2021 года.'''

    class Credits:
        def __init__(self):
            self.mes_text = '''С самого основания канала "КРОМО "Магистр" и до этого момента
каждый день, каждый час, каждую минуту
в поте лица, не покладая рук
над содержанием, оформлением, рубриками и всем тем, что вы видите
ТРУДЯТСЯ:

📢 <b>Анна Валерьевна Ланских</b>, куратор проекта
VK: <a href="https://zany21">@zany21</a>
Inst: <a href="https://www.instagram.com/annalanskih">@annalanskih</a>
О себе: специалист отдела имиджевых проектов и информационной политики КГУ, аналитик, креатор, SMM-специалист.
Много:
- смотрю о психологии, новинках в научном мире, фильмы и сериалы от Netflix;
- хожу пешком и слушаю подкасты и подборки от Яндекс.Музыки
- работаю в Магистре и КГУ.
Мечтаю много путешествовать, наполняться и пробовать новое!

💼 <b>Екатерина Боева</b>, менеджер по контенту
VK: <a href="https://vk.com/sadproblem_1">@sadproblem_1</a>
Inst: <a href="https://www.instagram.com/_sadproblem">@_sadproblem</a>
О себе: отбираю лучший контент для лучших пользователей!
Прекрасно снимаю и монтирую видео, увлекаюсь гуманитарными науками и всегда готова выслушать и помочь

💡 <b>Полина Смольянинова</b>, стратег
VK: <a href="https://aloapollinaria">@aloapollinaria</a>
Inst: <a href="https://www.instagram.com/p0p0shaa">@p0p0shaa</a>
О себе: баскетболистка, будущий журналист, самый душный экстраверт, мотиватор, обладатель кубка "Золотой голос Магистровского душа- 2021", любитель душевных посиделок, постоянный поставщик препаратов против негатива "Антивыгорин", "Настроениеподнимин" и "Полныйпозитивин", а вообще – просто хороший человек)

🎨 <b>Дарья Баулина</b>, дизайнер
VK: <a href="https://canular_d">@canular_d</a>
Inst: <a href="https://www.instagram.com/b_canular_d">@b_canular_d</a>
О себе: любительница детективов, кинематографа и долгих разговоров с интересными личностями, амбассадор искренности и восторженности, мадам "на любое слово отвечу песней" и просто хороший человек

🎲 <b>Вероника Якимова</b>, аналитик
VK: <a href="https://nikki_vskrto">@nikki_vskrto</a>
Inst: <a href="https://www.instagram.com/_n.i.kk.i._">@_n.i.kk.i._</a>
О себе: я творческий и креативный человек, который отдал 13 лет своей жизни спортивно-бальным танцам✨, всегда готова помочь с химией и объяснить её (пиши в директ!!) 🧬, обожаю книги по психологии и саморазвитию 🧠 , в дальнейшем мечтаю стать врачом и спасать жизни людей 👩‍⚕

📝 <b>Михаил Лобынцев</b>, копирайтер
VK: <a href="https://helloiameurofan">@helloiameurofan</a>
Inst: <a href="https://www.instagram.com/lobyntsevm">@lobyntsevm</a>
О себе: будущий юрист, душнила, фанат "Евровидения" и биатлона, стойкий переносчик учёбы, меломан, пенсионер и всё ещё одинокий человек – в одном лице

🤖 <b>Даниил Сазонов</b>, технический специалист
VK: <a href="https://dan_sazonov">@dan_sazonov</a>
Inst: <a href="https://www.instagram.com/dan_sazonov">@dan_sazonov</a>
О себе: постоянно включён ночной режим работы, питаюсь только кофе, окружён цифрами и программным кодом, больше десяти букв подряд не перевариваю!
'''

    class Santa:
        def __init__(self):
            self.on_start = '''<b>Привет и добро пожаловать в меню "Тайного Санты "Магистра"!</b>
Это анонимная игра, в которой каждый может стать Сантой (или, если хотите, Дедом Морозом) для случайного человека. Конечно же, он будет магистровцем!

<b>План такой:</b>
1️⃣ напиши, что ты хочешь получить в подарок;
2️⃣ реши, сможешь ли ты приехать на общелагерную встречу 12 декабря;
3️⃣ укажи, как тебя зовут и где ты живёшь;
4️⃣ затем наша система подберёт для тебя человека, которому ты сделаешь подарок!

P. S. Продолжая диалог с ботом, ты соглашаешься с нашей <a href="https://github.com/dan-sazonov/MagistrKurskBot/blob/master/legal_info/PRIVACY.md">Политикой конфиденциальности.</a>
'''
            self.ask_wishes = '''<b>Шаг 1.</b> Напиши в ответ на это сообщение свои пожелания по подарку. Что ты хочешь получить от своего Санты?'''
            self.ask_meeting = '''<b>Шаг 2.</b> Приедешь ли ты на общелагерную встречу 12 декабря? Нажми кнопку, которая соответствует твоему решению.

(За более подробной информацией обратись в канал "КРОМО "Магистр".)'''
            self.ask_address = '''<b>Шаг 3.</b> Напиши в ответ на это сообщение свой почтовый адрес в формате: индекс, город (или село/посёлок), улица, дом, квартира (при наличии)

Это нужно для того, чтобы доставить тебе подарок, если ты не сможешь приехать на встречу. Команда канала "КРОМО "Магистр" не собирает эту информацию в личных целях. Твой адрес будет знать ТОЛЬКО твой Тайный Санта. '''
            self.ask_name = '''<b>Шаг 4.</b>  Укажи в ответном сообщении свои фамилию, имя и отчество в именительном падеже.

Это не будет знать никто, кроме твоего Тайного Санты. Ему это понадобится, для того чтобы знать, кому отправить подарок.'''
            self.on_end = '''<b>Шаг 5.</b> Отлично! Наша система зарегистрировала тебя для участия в "Тайном Санте "Магистра".
Если ты захочешь отказаться от участия, отправь команду /end.

Мы напишем, кому ты будешь делать подарок, позже. Следи за обновлениями в канале!'''
            self.end = '''Очень жаль, что ты покидаешь игру! Для повторного участия отправь команду /santa'''
