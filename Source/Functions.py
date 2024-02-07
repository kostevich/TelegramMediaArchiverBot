
#==========================================================================================#
# >>>>> ПОДКЛЮЧЕНИЕ БИБЛИОТЕК И МОДУЛЕЙ <<<<< #
#==========================================================================================#

from dublib.Methods import RemoveFolderContent, ReadJSON
from .MessageBox import MessageBox


import datetime
import logging
import telebot
import shutil
import os

#==========================================================================================#
# >>>>> ОТПРАВКА СТАТИСТИКИ <<<<< #
#==========================================================================================#

def GenerateStatistics(Bot: telebot.TeleBot, UserID: str, ChatID: int, SizeObject: any, FlowObject):
    # Создание объекта класса MessageBox.
    MessageBoxObject = MessageBox(Bot = Bot)

    # Список названий файлов в директории пользователя.
    Files = os.listdir("Data/Files/" + str(UserID))
    
    # Размер всех скачанных файлов.
    Size = SizeObject.GetSizeDirectory(Files, str(UserID))

    # Словарь типов файлов.
    FileTypes = {
        "photo": 0,
        "video": 0,
        "document": 0,
        "audio": 0
    }

    # Словарь расширений файлов.
    FileExtensions = {
        "photo": ["jpg", "png", "webp", "jpeg", "ico", "gif", "svg"],
        "video": ["mp4", "avi", "wmw", "mkv", "3gp", "flv", "mov", "mpeg"],
        "audio": ["mp3", "ogg", "wav", "wma"]
    }
    
    # Для каждого файла.
    for File in Files:
        # Состояние: был ли типизирован файл.
        IsTyped = False

        # Для каждого типа расширений.
        for ExtensionType in FileExtensions.keys():
            # Расширение файла.
            FileExtension = File.split('.')[-1]
            
            # Если расширение файла принадлежит какому-то типу.
            if FileExtension in FileExtensions[ExtensionType]:
                # Инкремент количества файлов типа.
                FileTypes[ExtensionType] +=1
                # Переключение состояния типизации.
                IsTyped = True

        # Если тип не определён, то провести инкремент количества документов.
        if IsTyped == False:
            FileTypes["document"] +=1

    # Добавление статистики.
    count = str(FlowObject.CountMessagesBufer())
    size = str(SizeObject.Converter("Any", Size))
    photo = str(FileTypes["photo"])
    video = str(FileTypes["video"])
    documents = str(FileTypes["document"])
    audio = str(FileTypes["audio"])
    mistakes = str(len(ReadJSON("Data/Users/" + UserID + ".json")["UnloadedFiles"]))
    
    # Отправка статистики.
    MessageBoxObject.send(ChatID, "statistic", "statistic", {"count": count, "size": size, "photo": photo, "video": video, "documents": documents, "audio": audio, "mistakes": mistakes})
#==========================================================================================#
# >>>>> ОТПРАВКА АРХИВА  <<<<< #
#==========================================================================================#

def SendArchive(Bot: telebot.TeleBot, UserID: str, ChatID: int, UserDataObject: any):
    # Создание объекта класса MessageBox.
    MessageBoxObject = MessageBox(Bot = Bot)

    # Получение текущей даты.
    Date = datetime.datetime.now()

    # Форматирование названия файла.
    Date = str(Date).replace(':', '-').split('.')[0]
    
    # Состояние: удалась ли отправка архива.
    IsSended = False

    # Если существуют файлы для архивации.
    while len(os.listdir("Data/Files/" + UserID)) > 0:

        # Отправка сообщений пользователю.
        MessageBoxObject.send(ChatID, "archiving", "waiting")

        # Архивирование файлов пользователя.
        shutil.make_archive(f"Data/Archives/{UserID}/{Date}", "zip", "Data/Files/" + UserID)

        # Очистка файлов пользователя. 
        RemoveFolderContent("Data/Files/" + UserID)

        # Бинарное содержимое архива.
        BinaryArchive = None

        # Чтение архива.
        with open(f"Data/Archives/{UserID}/{Date}.zip", "rb") as FileReader:
            BinaryArchive = FileReader.read()
        
        # Отправка архива пользователю.
        Bot.send_document(ChatID, BinaryArchive, visible_file_name = f"{Date}.zip")

        # Логгирование.
        logging.info("Архив отправлен.")

        try: 
            # Получение списка словарей незагруженных файлов.
            UnloadedFiles = UserDataObject.GetInfo(UserID, "UnloadedFiles")

            # Отправка сообщения.
            MessageBoxObject.send(ChatID, "mistakes", "waiting")

            # Получение длины списка словарей незагруженных файлов.
            Lenth = len(UnloadedFiles)
            
            for Sequence in range(Lenth):
                
                if UnloadedFiles[0]["type"] == "document": 
                    # Отправка файлов, которые невозможно скачать.
                    Bot.send_document(ChatID, document = UnloadedFiles[0]["idfile"])
                    print(UnloadedFiles)
                    del UnloadedFiles[0]
                    print(UnloadedFiles)
                    UserDataObject.UpdateUser("UnloadedFiles", UnloadedFiles, "Update")
                
                if UnloadedFiles[0]["type"] == "audio":  
                    # Отправка файлов, которые невозможно скачать.
                    Bot.send_audio(ChatID, audio = UnloadedFiles[0]["idfile"])
                    print(UnloadedFiles)
                    del UnloadedFiles[0]
                    print(UnloadedFiles)
                    UserDataObject.UpdateUser("UnloadedFiles", UnloadedFiles, "Update")
                
                if UnloadedFiles[0]["type"] == "video": 
                    # Отправка файлов, которые невозможно скачать.
                    Bot.send_video(ChatID, video = UnloadedFiles[0]["idfile"])
                    print(UnloadedFiles)
                    del UnloadedFiles[0]
                    print(UnloadedFiles)
                    UserDataObject.UpdateUser("UnloadedFiles", UnloadedFiles, "Update")
                     
                if UnloadedFiles[0]["type"] == "photo": 
                    # Отправка файлов, которые невозможно скачать.
                    Bot.send_photo(ChatID, photo = UnloadedFiles[0]["idfile"])
                    print(UnloadedFiles)
                    del UnloadedFiles[0]
                    print(UnloadedFiles)
                    UserDataObject.UpdateUser("UnloadedFiles", UnloadedFiles, "Update")
                    
        except:
            # Логгирование.
            logging.info("Отправка файла не удалась")
       
        # Очистка архивов пользователя. 
        RemoveFolderContent("Data/Archives/" + UserID)
        
        # Переключение состояния.
        IsSended = True

    return IsSended


