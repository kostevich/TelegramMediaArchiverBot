
#==========================================================================================#
# >>>>> ПОДКЛЮЧЕНИЕ БИБЛИОТЕК И МОДУЛЕЙ <<<<< #
#==========================================================================================#

from dublib.Methods import RemoveFolderContent, ReadJSON


import datetime
import os
import shutil
import telebot

#==========================================================================================#
# >>>>> АРХИВ И ЕГО ОБРАБОТКА <<<<< #
#==========================================================================================#
        
class Archive():

#==========================================================================================#
# >>>>> ОТПРАВКА АРХИВА  <<<<< #
#==========================================================================================#

    def __init__(self) -> None:
        pass

    def SendArchive(self, Bot: telebot.TeleBot, UserID: str, ChatID: int, FlowObject: any) -> bool:

        # Получение текущей даты.
        self.Date = datetime.datetime.now()

        # Форматирование названия файла.
        self.Date = str(self.Date).replace(':', '-').split('.')[0]
        
        self.WaitingArchive(FlowObject, UserID, Bot)

        # Состояние: удалась ли отправка архива.
        IsSended = False

    def WaitingArchive(self, FlowObject, UserID, Bot, ChatID):
        # Если существуют файлы для архивации.
        while len(os.listdir("Data/Files/" + UserID)) > 0:
            if len(FlowObject._Flow__MessagesBufer) <= 0:
                # Архивирование файлов пользователя.
                shutil.make_archive(f"Data/Archives/{UserID}/{self.Date}", "zip", "Data/Files/" + UserID)

                # Очистка файлов пользователя. 
                RemoveFolderContent("Data/Files/" + UserID)

                # Бинарное содержимое архива.
                BinaryArchive = None

                # Чтение архива.
                with open(f"Data/Archives/{UserID}/{self.Date}.zip", "rb") as FileReader:
                    BinaryArchive = FileReader.read()

                # Отправка архива пользователю.
                Bot.send_document(ChatID, BinaryArchive, visible_file_name = f"{self.Date}.zip")

                # Очистка архивов пользователя. 
                RemoveFolderContent("Data/Archives/" + UserID)
                
                # Переключение состояния.
                IsSended = True
                
            else:
                Bot.send_message(ChatID, "❗ Не все ваши файлы сейчас находятся в архиве. Подождите...")

        return IsSended