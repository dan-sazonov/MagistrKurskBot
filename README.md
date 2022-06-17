# MagistrKurskBot
[![GitHub](https://img.shields.io/github/license/dan-sazonov/MagistrKurskBot)](https://github.com/dan-sazonov/MagistrKurskBot/blob/master/LICENSE.md)&nbsp;&nbsp;
![OpenSource](https://img.shields.io/badge/Open%20Source-%E2%99%A5-red)<br>

**Чат-бот для телеграм-канала [КРОМО "Магистр"](https://t.me/magistrKursk).**

## 📝 Техническое задание
- [X] Переписать текущий функционал на aiogram
- [X] Создать бота на новом ID, оформить UI
- [X] Задеплоить бота, поменять ссылки в соцсетях Магистра
- [X] Запилить [тайного санту](./Идеи/санта.md)
- [X] Релиз версии 2
- [X] Запилить [анонимную почту](./Идеи/1402.md) на 14 февраля
- [ ] Разработать спам-фильтр, прикрутить к коментам
- [ ] Создать чат канала, прикрутить спам-фильтр к нему
- [ ] Обсудить новый функционал бота, возможности развития
- [ ] Сделать новые стикеры

## 🛠 Стэк
- Python3 + aiogram
- **БД:** PostgreSQL
- **Облако:** Heroku

Разработка идет на ветке `master`. На ветке `prod-v1` последний стабильный релиз v1.x.x. Разработка данной версии прекращена, актуальные релизы сливаются в `prod-v2`.  
Перед запуском на локалке необходимо поставить пакеты из `requirements.txt` и создать переменные окружения `BOT_TOKEN` и `DATABASE_URL` со значением токена бота и URI бд соответственно.

## 🎯 Совместимость
Версии `v2.` разарбатываются под версию интерпретатора Python `3.8.2`, также гарантируется совместимость с версией `3.9.0`.<br>
**ОС:** _Ubuntu Server 18.04 x64_, также протестирован на _Windows 10 Pro x64_

## 🤝 Хотите сотрудничать?
Если вы обнаружили ошибку в коде, или знаете более оптимальное решение, откройте
[ишью](https://github.com/dan-sazonov/MagistrKurskBot/issues). Вы можете взять ишью, и сказать мне, что работаете над ним. 
Если вы хотите предложить свое решение, сделайте [пулл-реквест](https://github.com/dan-sazonov/MagistrKurskBot/pulls). 

## 👨‍💻 Автор
Автор репозитория и кода - [@dan-sazonov](https://github.com/dan-sazonov). <br>
**Связаться со мной:**<br>
- <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/768px-Telegram_logo.svg.png" width=16 height=16> Telegram:<a href="https://t.me/dan_sazonov"> @dan_sazonov</a>  
- <img src="https://upload.wikimedia.org/wikipedia/commons/2/21/VK.com-logo.svg" width=16 height=16> VK:<a href="https://vk.com/dan_sazonov"> @dan_sazonov</a> 
- 📩 E-mail: [`dan_sazonov@vk.com`](mailto:/dan_sazonov@vk.com)

## 📜 Лицензия
Весь код распространяется по лицензии [GPL-3.0 License](https://github.com/dan-sazonov/MagistrKurskBot/LICENSE.md).<br>
Подробнее смотри в файле.
