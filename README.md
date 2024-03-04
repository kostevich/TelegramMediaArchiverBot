# Telegram Media Archiver Bot
**Telegram Media Archiver Bot** – это [Telegram](https://telegram.org) - бот  для автоматической архивации медиавложений из ваших сообщений. С его помощью вы легко сможете скачать сотни файлов одним нажатием кнопки.

# Порядок установки и использования
1. Загрузить последний релиз. Распаковать.
2. Установить [Python](https://www.python.org/downloads/) версии не старше 3.10. Рекомендуется добавить в PATH.
3. В среду исполнения установить следующие пакеты: [dublib](https://github.com/DUB1401/dublib), [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI).
```
pip install dublib
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

![image](https://github.com/kostevich/TelegramMediaArchiverBot/assets/109979502/584c8560-80bc-4648-9922-ffa8ae17df6c)


**Обработка команды statistics:**

![image](https://github.com/kostevich/TelegramMediaArchiverBot/assets/109979502/00ca8012-c869-440a-a308-1a893437c2b6)

**Обработка команды clear:**

![image](https://github.com/kostevich/TelegramMediaArchiverBot/assets/109979502/43eb152f-bf33-419b-84c6-397ebc24cc02)

**Обработка команды archive:**

![image](https://github.com/kostevich/TelegramMediaArchiverBot/assets/109979502/631ce178-5d5f-47a4-a4da-80dd4103661b)

_Copyright © Kostevich Irina. 2023-2024._
