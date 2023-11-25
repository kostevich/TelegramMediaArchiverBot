# Telegram Media Archiver Bot
**Telegram Media Archiver Bot** – это бот [Telegram](https://telegram.org) для автоматической архивации медиавложений из ваших сообщений. С его помощью вы легко сможете скачать сотни файлов одним нажатием кнопки.

# Порядок установки и использования
1. Загрузить последний релиз. Распаковать.
2. Установить [Python](https://www.python.org/downloads/) версии не старше 3.11. Рекомендуется добавить в PATH.
3. В среду исполнения установить следующие пакеты: [dublib](https://github.com/DUB1401/dublib), [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI).
```
pip install git+https://github.com/DUB1401/dublib#egg=dublib
pip install pyTelegramBotAPI
```
Либо установить сразу все пакеты при помощи следующей команды, выполненной из директории скрипта.
```
pip install -r Requirements.txt
```
4. Настроить бота путём редактирования _Settings.json_.
5. Запустить файл _Main.py_.
6. Перейти в чат с ботом, токен которого указан в настройках, и следовать его инструкциям.

# Settings.json
```JSON
"token": ""
```
Сюда необходимо занести токен бота Telegram (можно получить у [BotFather](https://t.me/BotFather)).

# Добавление команд 

Можно указать в настройках бота в [BotFather](https://t.me/BotFather).

Start - start working.

Statistics - send file statistics.

Archive - archive files and send it.

# Пример работы

![Обработка команды start](photo_2023-10-17_21-21-29.jpg)

![Вывод команд](image_2023-10-17_21-17-26-1.png)

![Обработка команды statistics и archive](image-2.png)

_Copyright © Kostevich Irina. 2023._
