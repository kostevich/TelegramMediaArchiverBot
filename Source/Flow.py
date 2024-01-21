
#==========================================================================================#
# >>>>> ПОДКЛЮЧЕНИЕ БИБЛИОТЕК И МОДУЛЕЙ <<<<< #
#==========================================================================================#

from dublib.Methods import ReadJSON
from threading import Thread
from Source.Functions import VariableFilesNotSave, VariablePremium


import logging
import requests

#==========================================================================================#
# >>>>> ПОТОК И ЕГО ОБРАБОТКА <<<<< #
#==========================================================================================#

class Flow:

    #==========================================================================================#
    # >>>>> КОНСТРУКТОР <<<<< #
    #==========================================================================================#

    def __init__(self):
        # Создание потока.
        self.__Download = Thread(target = self.__DownloadThread)

        # Очередь медиафайлов.
        self.__MessagesBufer = list()

        # Запуск очереди.
        self.__Download.start()

        # Состояния очереди.
        self.CheckEmptyThread = str()

    #==========================================================================================#
    # >>>>> ОБРАБОТКА ПОТОКОВЫХ ДАННЫХ <<<<< #
    #==========================================================================================#
        
    def __DownloadThread(self):
        # Логгирование.
        logging.info("Поток запущен.")
        
        # Пока сообщение не отправлено.
        while True:
            # Если в очереди на загрузке есть медиафайлы.
            if len(self.__MessagesBufer) > 0:
                # Сохранение состояния очереди.
                self.CheckEmptyThread = False

                # Скачиваем файл.
                self.DownloadFile(self.__MessagesBufer)

            else: 
                # Сохранение состояния очереди.
                self.CheckEmptyThread = True

    #==========================================================================================#
    # >>>>> ДОБАВЛЕНИЕ ФАЙЛА В ОЧЕРЕДЬ МЕДИАФАЙЛОВ <<<<< #
    #==========================================================================================#   
                   
    def AddFileInfo(self, FileInfo: any, UserDataObject: any, Settings: dict):
        # Добавление файла в список.
        self.__MessagesBufer.append(FileInfo)
        self.Settings = Settings
        self.UserDataObject = UserDataObject

    #==========================================================================================#
    # >>>>> ЗАГРУЗКА ФАЙЛОВ <<<<< #
    #==========================================================================================# 
           
    def DownloadFile(self, MessagesBufer: list):
        # Получение данных файла.
        try:
            # Расширение файла.
            FileType = "." + MessagesBufer[0].file_path.split('.')[-1]

            # Загрузка файла.
            Response = requests.get("https://api.telegram.org/file/bot" + self.Settings["token"] + f"/{ MessagesBufer[0].file_path}")
            
            # Сохранение файла.
            with open(f"Data/Files/{self.UserDataObject.getUserID()}/" + str(MessagesBufer[0].file_unique_id) + FileType, "wb") as FileWriter:
                FileWriter.write(Response.content)

                # Размер всех скачанных файлов.
                UpdatingSize = ReadJSON("Data/Users/" + self.UserDataObject.getUserID() + ".json")["Size"] + MessagesBufer[0].file_size/1024

                # Запись в json.
                self.UserDataObject._UserData__UpdateSizeUser(UpdatingSize, VariableFilesNotSave(self.UserDataObject), VariablePremium(self.UserDataObject))
            
                # Удаление элемента из списка.
                MessagesBufer.remove(MessagesBufer[0])  
                
        except: 
            # Логгирование.
            logging.error("Не получилось загрузить файл.") 