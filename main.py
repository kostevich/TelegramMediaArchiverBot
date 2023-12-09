 #!/usr/bin/python

#==========================================================================================#
# >>>>> ПОДКЛЮЧЕНИЕ БИБЛИОТЕК И МОДУЛЕЙ <<<<< #
#==========================================================================================#

from dublib.Methods import CheckPythonMinimalVersion, MakeRootDirectories, ReadJSON
from Source.Functions import *
from Source.Sizes import *
from Source.UserData import UserData
from telebot import types


import telebot

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ СКРИПТА <<<<< #
#==========================================================================================#

# Проверка поддержки используемой версии Python.
CheckPythonMinimalVersion(3, 11)

# Создание папки в корневой директории.
MakeRootDirectories(["Data"])

#==========================================================================================#
# >>>>> ЧТЕНИЕ НАСТРОЕК <<<<< #
#==========================================================================================#

# Чтение настроек.
Settings = ReadJSON("Settings.json")

# Если токен не указан, выбросить исключение.
if type(Settings["token"]) != str or Settings["token"].strip() == "":
    raise Exception("Invalid Telegram bot token.")

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ БОТА <<<<< #
#==========================================================================================#

# Токен для работы определенного бота телегамм.
Bot = telebot.TeleBot(Settings["token"])

#==========================================================================================#
# >>>>> ОБРАБОТКА КОМАНД: ARCHIVE, START, STATISTICS <<<<< #
#==========================================================================================#


#==========================================================================================#
# >>>>> ОБРАБОТКА КОМАНДЫ ARCHIVE <<<<< #
#==========================================================================================#

# Обрабатывает команду: archive.
@Bot.message_handler(commands=["archive"])
def ProcessCommandStart(Message: types.Message):
    # Запрос данных пользователя.
    UserDataObject = UserData(Message.from_user.id)

    # Если не удалась отправка архива.
    if SendArchive(Bot, UserDataObject.getUserID(), Message.chat.id) == False:
        # Отправить инструкции пользователю.
        Bot.send_message(Message.chat.id, "❗ Вы не отправили мне ни одного файла.")

#==========================================================================================#
# >>>>> ОБРАБОТКА КОМАНДЫ START <<<<< #
#==========================================================================================#
    
# Обрабатывает команду: start.
@Bot.message_handler(commands=["start"])
def ProcessCommandStart(Message: types.Message):
    # Запрос данных пользователя.
    UserDataObject = UserData(Message.from_user.id)

    # Отправка приветствия.
    Bot.send_message(
        Message.chat.id,
        "Пришлите мне сообщения, содержащие медиафайлы, и я соберу их для вас в один архив\.\n\n*Список команд\:*\n/start – начать работу с ботом;\n/statistics – вывести статистику типов медиафайлов;\n/archive – отправить архив с медиафайлами\.",
        parse_mode = "MarkdownV2"
    )

#=========================================================================================#
# >>>>> ОБРАБОТКА КОМАНДЫ STATISTICS <<<<< #
#==========================================================================================#

# Обрабатывает команду: statistics.
@Bot.message_handler(commands=["statistics"])
def ProcessCommandStart(Message: types.Message):
    # Запрос данных пользователя.
    UserDataObject = UserData(Message.from_user.id)

    # Отправка статистики медиафайлов.
    GenerateStatistics(Bot, UserDataObject.getUserID(), Message.chat.id, SizeDirectory)

#=========================================================================================#
# >>>>> ОБРАБОТЧИК МЕДИАФАЙЛОВ <<<<< #
#==========================================================================================#

# Обработчик фото, видео, аудио, документов.
@Bot.message_handler(content_types=["photo", "video", "audio", "document"])
def ProcessFileUpload(Message: types.Message):
    # Запрос данных пользователя.
    UserDataObject = UserData(Message.from_user.id)
    
    # ID файла.
    FileID = None

    # Если тип файла – фото.
    if Message.content_type == "photo":
        FileID = Message.photo[-1].file_id

    # Если тип файла – фото.
    elif Message.content_type == "video":
        FileID = Message.video.file_id

    # Если тип файла – фото.
    elif Message.content_type == "audio":
        FileID = Message.audio.file_id

    # Если тип файла – фото.
    elif Message.content_type == "document":
        FileID = Message.document.file_id

    # Загрузка файла.
    DownloadFile(Bot, Settings, FileID, UserDataObject.getUserID(), Message, SizeDirectory)

# Запуск обработки запросов Telegram.
Bot.polling(none_stop = True)