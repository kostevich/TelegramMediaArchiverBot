
#==========================================================================================#
# >>>>> ПОДКЛЮЧЕНИЕ БИБЛИОТЕК И МОДУЛЕЙ <<<<< #
#==========================================================================================#

from dublib.Methods import CheckPythonMinimalVersion, MakeRootDirectories, ReadJSON, RemoveFolderContent
from Source.Functions import GenerateStatistics, SendArchive
from Source.MessageBox import MessageBox
from Source.UserData import UserData
from Source.Sizer import Sizer
from Source.Flow import Flow
from telebot import types


import logging
import telebot

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ СКРИПТА <<<<< #
#==========================================================================================#

# Проверка поддержки используемой версии Python.
CheckPythonMinimalVersion(3, 10)

# Создание папки в корневой директории.
MakeRootDirectories(["Data/Files", "Data/Archives", "Data/Users"])

#==========================================================================================#
# >>>>> НАСТРОЙКА ЛОГИРОВАНИЯ <<<<< #
#==========================================================================================#

# Создание настроек логирования.
logging.basicConfig(level=logging.INFO, encoding="utf-8", filename="LOGING.log", filemode="w",
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

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
# >>>>> СОЗДАНИЕ ОБЪЕКТОВ <<<<< #
#==========================================================================================#

# Создание объекта класса Flow.
FlowObject = Flow(Settings)

# Создание объекта класса Sizer.
SizerObject = Sizer()

# Создание объекта класса MessageBox.
MessageBoxObject = MessageBox(bot = Bot)

#==========================================================================================#
# >>>>> ОБРАБОТКА КОМАНДЫ ARCHIVE <<<<< #
#==========================================================================================#

@Bot.message_handler(commands=["archive"])
def ProcessCommandArchive(Message: types.Message):
    # Запрос данных пользователя.
    UserDataObject = UserData(Message.from_user.id)

    # Если очередь отправки файлов пуста.
    if FlowObject.EmptyFlowStatus() == True:
        # Если не удалась отправка архива.
        if SendArchive(Bot, UserDataObject.GetUserID(), Message.chat.id, UserDataObject) == False:
            # Отправка сообщения: пользователь не отправил ни одного файла.
            MessageBoxObject.send(Message.chat.id, "no-files", "error")

    else:
        # Отправить инструкции пользователю.
        Bot.send_message(Message.chat.id, "⏳\n\n Идёт загрузка файлов. Повторите попытку позже...")

#==========================================================================================#
# >>>>> ОБРАБОТКА КОМАНДЫ ClEAR <<<<< #
#==========================================================================================#

@Bot.message_handler(commands=["clear"])
def ProcessCommandArchive(Message: types.Message):
    # Запрос данных пользователя.
    UserDataObject = UserData(Message.from_user.id)

    # Есть ли файлы пользователя в потоке.
    if FlowObject.CheckUserFilesPresence(UserDataObject.GetUserID()) == False:
        # Удаление файлов пользователя.
        RemoveFolderContent("Data/Files/" + UserDataObject.GetUserID())

        # Отправка сообщения.
        Bot.send_message(Message.chat.id, "✅\n\n Сборка файлов очищена.")

    else:
        # Отправка сообщения.
        Bot.send_message(Message.chat.id, "⏳\n\n Повторите попытку позже.")
       

#==========================================================================================#
# >>>>> ОБРАБОТКА КОМАНДЫ START <<<<< #
#==========================================================================================#

@Bot.message_handler(commands=["start"])
def ProcessCommandStart(Message: types.Message):
    # Отправка приветствия.
    Bot.send_message(
        Message.chat.id,
        "ℹ️ Пришлите мне сообщения, содержащие медиафайлы, и я соберу их для вас в один архив\.\n\n*Список команд\:*\n/start – начать работу с ботом;\n/clear – сбросить архивирование;\n/statistics – вывести статистику типов медиафайлов;\n/archive – отправить архив с медиафайлами\.",
        parse_mode = "MarkdownV2"
    )

#=========================================================================================#
# >>>>> ОБРАБОТКА КОМАНДЫ STATISTICS <<<<< #
#==========================================================================================#

@Bot.message_handler(commands=["statistics"])
def ProcessCommandStatistics(Message: types.Message):
    # Запрос данных пользователя.
    UserDataObject = UserData(Message.from_user.id)

    # Отправка статистики медиафайлов.
    GenerateStatistics(Bot, UserDataObject.GetUserID(), Message.chat.id, SizerObject, FlowObject)

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
        
        # Логгирование.
        logging.info("Получены данные файла.")
        
        # Если размер файла меньше 20 MB.
        if SizerObject.CheckSize(FileInfo) == True:
            # Размер всех файлов, которые будут скачаны.
            UpdatingSize = UserDataObject.GetInfo(UserDataObject.GetUserID(), "Size") + SizerObject.Converter("KB", FileInfo.file_size)
            
            # Если размер всех скачанных файлов меньше 20 MB.
            if UpdatingSize < 20480:
                # Запись в json.
                UserDataObject.UpdateUser("Size", UpdatingSize, "Update")
               
                # Добавление файла в очередь.
                FlowObject.AddFileInfo(FileInfo, UserDataObject)
                
                logging.info("Файл добавлен в очередь.")
    
            else:
                # Добавление незагруженных файлов.
                UserDataObject.UpdateUser("UnloadedFiles", {
                "file": FileID,
                "userid": UserDataObject.GetUserID(), 
                "type": Message.content_type

            }, "Add")

    except: 
        # Добавление незагруженных файлов.
        UserDataObject.UpdateUser("UnloadedFiles", {
                "file": FileID,
                "userid": UserDataObject.GetUserID(), 
                "type": Message.content_type
            }, "Add")

# Запуск обработки запросов Telegram.
Bot.polling(none_stop = True)