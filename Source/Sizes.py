
#==========================================================================================#
# >>>>> ПОДКЛЮЧЕНИЕ БИБЛИОТЕК И МОДУЛЕЙ <<<<< #
#==========================================================================================#

from dublib.Methods import WriteJSON


import logging

#==========================================================================================#
# >>>>> СОЗДАНИЕ РАЗМЕРА ФАЙЛОВ <<<<< #
#==========================================================================================#

class Size:

    # Конструктор.    
    def __init__(self):
        self.Units = ['B', 'KB', 'MB', 'GB']
        self.Size = str()

    # Проверка размера.
    def CheckSize(self, FileInfo: any)-> bool:
        # Состояние.
        IsChecked = False

        # Размер в KB.
        SizeFile = FileInfo.file_size/1024

        # Если размер больше 20 MB.
        if SizeFile < 20480:
            # Состояние.
            IsChecked = True

            # Логгирование.
            logging.info(f"Размер файла: {SizeFile}.")
        
        return IsChecked 

    
    def Converter(self, Value) -> str():
        if Value > 1000:
            if Value/1024 > 1024:
                if Value/1024 > 1024:
                    self.Size = str(Value) + self.Units[3]
            else: 
                self.Size = str(Value) + self.Units[2]
        else:
            self.Size = str(Value) + self.Units[1]
        return self.Size
                
        

# Создание объекта класса.
SizeObject = Size()