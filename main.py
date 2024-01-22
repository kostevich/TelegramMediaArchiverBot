#!/usr/bin/python

#==========================================================================================#
# >>>>> ПОДКЛЮЧЕНИЕ БИБЛИОТЕК И МОДУЛЕЙ <<<<< #
#==========================================================================================#

from dublib.Methods import CheckPythonMinimalVersion, MakeRootDirectories, ReadJSON
from Source.Flow import Flow
from Source.Functions import *
from Source.Size import Size
from Source.UserData import UserData
from Source.Manager import Manager
from telebot import types


import logging
import telebot

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ СКРИПТА <<<<< #
#==========================================================================================#

# Проверка поддержки используемой версии Python.
CheckPythonMinimalVersion(3, 11)

# Создание папки в корневой директории.
MakeRootDirectories(["Data/Files", "Data/Archives", "Data/Users"])

#==========================================================================================#
# >>>>> ЧТЕНИЕ НАСТРОЕК <<<<< #
#==========================================================================================#

# Чтение настроек.
Settings = ReadJSON("Settings.json")

# Если токен не указан, выбросить исключение.
if type(Settings["token"]) != str or Settings["token"].strip() == "":
    raise Exception("Invalid Telegram bot token.")

#==========================================================================================#
# >>>>> НАСТРОЙКА ЛОГИРОВАНИЯ <<<<< #
#==========================================================================================#

logging.basicConfig(level=logging.INFO, encoding="utf-8", filename="LOGING.log", filemode="w",
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ БОТА <<<<< #
#==========================================================================================#

# Токен для работы определенного бота телегамм.
Bot = telebot.TeleBot(Settings["token"])

#==========================================================================================#
# >>>>> СОЗДАНИЕ ЭКЗЕМПЛЯРОВ КЛАССА <<<<< #
#==========================================================================================#

# Создание экземпляра класса Flow.
FlowObject = Flow()

# Создание экземпляра класса Size.
SizeObject = Size()

# Создание экземпляра класса Size.
ManagerObject = Manager()

#==========================================================================================#
# >>>>> ОБРАБОТКА КОМАНДЫ ARCHIVE <<<<< #
#==========================================================================================#

@Bot.message_handler(commands=["archive"])
def ProcessCommandStart(Message: types.Message):
    # Запрос данных пользователя.
    UserDataObject = UserData(Message.from_user.id)

    if FlowObject.CheckEmptyThread == True:
        # Если не удалась отправка архива.
        if SendArchive(Bot, UserDataObject.getUserID(), Message.chat.id, FlowObject) == False:
            # Отправить инструкции пользователю.
            Bot.send_message(Message.chat.id, "❗ Вы не отправили мне ни одного файла.")
    
    else:
        # Отправить инструкции пользователю.
        Bot.send_message(Message.chat.id, "❗️ Не все ваши файлы сейчас находятся в архиве. Подождите...")

#==========================================================================================#
# >>>>> ОБРАБОТКА КОМАНДЫ START <<<<< #
#==========================================================================================#

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

@Bot.message_handler(commands=["statistics"])
def ProcessCommandStart(Message: types.Message):
    # Запрос данных пользователя.
    UserDataObject = UserData(Message.from_user.id)

    # Отправка статистики медиафайлов.
    GenerateStatistics(Bot, UserDataObject.getUserID(), Message.chat.id, SizeObject)

#=========================================================================================#
# >>>>> ОБРАБОТЧИК МЕДИАФАЙЛОВ <<<<< #
#==========================================================================================#

@Bot.message_handler(content_types=["photo", "video", "audio", "document"])
def ProcessFileUpload(Message: types.Message):
    # Запрос данных пользователя.
    UserDataObject = UserData(Message.from_user.id)
    
    # ID файла.
    FileID = None

    # Если тип файла – фото.
    if Message.content_type == "photo":
        FileID = Message.photo[-1].file_id

    # Если тип файла – видео.
    elif Message.content_type == "video":
        FileID = Message.video.file_id

    # Если тип файла – аудио.
    elif Message.content_type == "audio":
        FileID = Message.audio.file_id

    # Если тип файла – документ.
    elif Message.content_type == "document":
        FileID = Message.document.file_id
        
    
    try:
        # Получение данных файла.
        FileInfo = Bot.get_file(FileID)
        
        # Если размер файла меньше 20 MB.
        if SizeObject.CheckSize(FileInfo) == True:
            # Размер всех файлов, которые будут скачаны.
            UpdatingSize = ReadJSON("Data/Users/" + UserDataObject.getUserID() + ".json")["Size"] + (float(FileInfo.file_size)/1024)
            # Если размер всех скачанных файлов меньше 20 MB.
            if UpdatingSize < 20480:

                # Запись в json.
                UserDataObject._UserData__UpdateSizeUser(UpdatingSize, VariableFilesNotSave(UserDataObject), VariablePremium(UserDataObject))

                # Добавление файла в очередь.
                FlowObject.AddFileInfo(FileInfo, UserDataObject, Settings)

                logging.info("Добавление файла в очередь.")

            # Посылаем сообщение.    
            else:
                logging.info("1. FileID.")

                Bot.send_message(
            Message.chat.id,
            "Вы привысили лимит скачиваний файлов\. Обратитесь в поддержку\.",
            parse_mode = "MarkdownV2"
        )
                

    except: 
        ManagerObject.ReceivingUnloadedFiles(UserDataObject.getUserID(), FileID)
        logging.info("3. FileID.")



# Запуск обработки запросов Telegram.
Bot.polling(none_stop = True)