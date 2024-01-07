 #!/usr/bin/python

#==========================================================================================#
# >>>>> ПОДКЛЮЧЕНИЕ БИБЛИОТЕК И МОДУЛЕЙ <<<<< #
#==========================================================================================#

from dublib.Methods import CheckPythonMinimalVersion, MakeRootDirectories, ReadJSON
from Source.Functions import *
from Source.Sizes import *
from Source.UserData import UserData
from telebot import types
from threading import Thread


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

logging.basicConfig(level=logging.INFO, filename="LOGING.log", filemode="w")

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ БОТА <<<<< #
#==========================================================================================#

# Токен для работы определенного бота телегамм.
Bot = telebot.TeleBot(Settings["token"])

class Order:
    # Конструктор: задаёт глобальные настройки, обработчик конфигураций и менеджер подключений к ботам.
    def __init__(self, Settings):
        # Поток загрузки файла.
        self.__Download = Thread(target = self.__SenderThread, name = "Отправка сообщений")
        # Очередь отложенных сообщений.
        self.__MessagesBufer = list()
        self.__Download.start()
        self.Settings = Settings
          
    def AddFileInfo(self, FileInfo, UserDataObject):
        self.__MessagesBufer.append(FileInfo)
        self.UserDataObject = UserDataObject

    # Обрабатывает очередь сообщений.
    def __SenderThread(self):
        # Вывод информации о запуске процесса.
        logging.info("Поток запущен.")
        
        # Пока сообщение не отправлено.
        while True:
            # Если в очереди на отправку есть сообщения.
            if len(self.__MessagesBufer) > 0:
                DownloadFile(self.__MessagesBufer, Settings, self.UserDataObject)
                logging.info("Загрузка файлов.")
        

OrderObject = Order(Settings)    

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
    GenerateStatistics(Bot, UserDataObject.getUserID(), Message.chat.id)

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
    
    FileInfo = Bot.get_file(FileID) 
    
    if SizeObject.CheckSize(FileInfo) == True:
        # Добавление файла в очередь.
        OrderObject.AddFileInfo(FileInfo, UserDataObject)
        logging.info("Добавление файла в очередь.")


# Запуск обработки запросов Telegram.
Bot.polling(none_stop = True)