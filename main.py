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

logging.basicConfig(level=logging.INFO, encoding="utf-8", filename="LOGING.log", filemode="w",
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ БОТА <<<<< #
#==========================================================================================#

# Токен для работы определенного бота телегамм.
Bot = telebot.TeleBot(Settings["token"])

class Order:
    # Конструктор: задаёт глобальные настройки, обработчик конфигураций и менеджер подключений к ботам.
    def __init__(self, Settings: dict):
        # Поток загрузки файла.
        self.__Download = Thread(target = self.__SenderThread, name = "Отправка сообщений")

        # Очередь отложенных сообщений.
        self.__MessagesBufer = list()

        # Запуск очереди.
        self.__Download.start()

        # Настройки бота.
        self.Settings = Settings
          
    def AddFileInfo(self, FileInfo: any, UserDataObject: UserData):
        # Добавление файла в список.
        self.__MessagesBufer.append(FileInfo)

        # Создание объекта класса.
        self.UserDataObject = UserDataObject

    # Обрабатывает очередь сообщений.
    def __SenderThread(self):
        # Логгирование.
        logging.info("Поток запущен.")
        
        # Пока сообщение не отправлено.
        while True:
            # Если в очереди на отправку есть сообщения.
            if len(self.__MessagesBufer) > 0:
                # Скачиваем файл.
                DownloadFile(self.__MessagesBufer, Settings, self.UserDataObject)

                # Логгирование.
                logging.info("Загрузка файлов.")
        
# Создание объекта класса.
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
    GenerateStatistics(Bot, UserDataObject.getUserID(), Message.chat.id, UserDataObject)

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
    
    # Получение данных файла.
    FileInfo = Bot.get_file(FileID) 
    
    # Если размер файла меньше 20 MB.
    if SizeObject.CheckSize(FileInfo) == True:
        # Если размер всех скачанных файлов меньше 20 MB.
        if ReadJSON("Data/Users/" + UserDataObject.getUserID() + ".json")["Size"]< 20480:
            # Добавление файла в очередь.
            OrderObject.AddFileInfo(FileInfo, UserDataObject)
            
            # Логгирование.
            logging.info("Добавление файла в очередь.")

        # Посылаем сообщение.    
        else:
            Bot.send_message(
        Message.chat.id,
        "Вы привысили лимит скачиваний файлов\. Обратитесь в поддержку\.",
        parse_mode = "MarkdownV2"
    )
            
    # Посылаем сообщение. 
    else: 
        Bot.send_message(
        Message.chat.id,
        "Пока файлы размером больше 20 мб недоступны для скачивания\. Такая функция будет доступна в скором времени\.",
        parse_mode = "MarkdownV2"
    )


# Запуск обработки запросов Telegram.
Bot.polling(none_stop = True)