# Telegram Media Archiver Bot
**Telegram Media Archiver Bot** – это [Telegram](https://telegram.org) - бот  для автоматической архивации медиавложений из ваших сообщений. С его помощью вы легко сможете скачать сотни файлов одним нажатием кнопки.

# Порядок установки и использования
1. Загрузить последний релиз. Распаковать.
2. Установить [Python](https://www.python.org/downloads/) версии не старше 3.11. Рекомендуется добавить в PATH.
3. В среду исполнения установить следующие пакеты: [dublib](https://github.com/DUB1401/dublib), [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI).
```
pip install git+https://github.com/DUB1401/dublib
pip install pyTelegramBotAPI
```
Либо установить сразу все пакеты при помощи следующей команды, выполненной из директории скрипта.
```
pip install -r requirements.txt
```
4. Настроить бота путём редактирования [_Settings.json_](#Settings).
5. Можно добавить команды в бота, для удобства работы [(бот будет работать и без этой настройки)](#AddCommands).
6. Запустить файл _main.py_.
7. Перейти в чат с ботом, токен которого указан в настройках, и следовать его инструкциям.

<a name="Settings"></a> 
# Settings.json
```JSON
"token": ""
```
Сюда необходимо занести токен бота Telegram (можно получить у [BotFather](https://t.me/BotFather)).

<a name="AddCommands"></a> 
# Добавление команд 
Можно указать в настройках бота в [BotFather](https://t.me/BotFather).

Start - start working.

Сlear - reset the archive build.

Statistics - send file statistics.

Archive - archive files and send it.

# Пример работы
**Обработка команды start:**

![photo_2023-10-17_21-21-29](https://github.com/kostevich/TelegramMediaArchiverBot/assets/109979502/6451fdcf-2c9c-47d9-9eb9-be94e1f3448f)

**Вывод команд:**

![image_2023-10-17_21-17-26-1](https://github.com/kostevich/TelegramMediaArchiverBot/assets/109979502/8e018e47-fa02-4e67-a56f-4e006c3349f5)

**Обработка команды statistics и archive:**

![image-2](https://github.com/kostevich/TelegramMediaArchiverBot/assets/109979502/ed863b9b-9d90-4f68-923f-9a388d40e695)

_Copyright © Kostevich Irina. 2023._
