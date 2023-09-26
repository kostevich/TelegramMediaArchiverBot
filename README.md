# Telegram Media Archiver Bot
**Telegram Media Archiver Bot** – это бот [Telegram](https://telegram.org) для автоматической архивации медиа-вложений из ваших сообщений. С его помощью вы легко сможете скачать сотни изображений одним нажатием кнопки.

## Порядок установки и использования
1. Загрузить последний релиз. Распаковать.
2. Установить Python версии не старше 3.10. Рекомендуется добавить в PATH.
3. В среду исполнения установить следующие пакеты: [dublib](https://github.com/DUB1401/dublib), [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI).
```
pip install git+https://github.com/DUB1401/dublib#egg=dublib
pip install pyTelegramBotAPI
```
Либо установить сразу все пакеты при помощи следующей команды, выполненной из директории скрипта.
```
pip install -r requirements.txt
```
4. Настроить бота путём редактирования _Settings.json_.
5. Запустить файл _main.py_.
6. Перейти в чат с ботом, токен которого указан в настройках, и следовать его инструкциям.

# Settings.json
```JSON
"token": ""
```
Сюда необходимо занести токен бота Telegram (можно получить у [BotFather](https://t.me/BotFather)).

_Copyright © Kostevich Irina. 2023._
