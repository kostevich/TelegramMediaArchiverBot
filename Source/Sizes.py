#==========================================================================================#
# >>>>> ПОДКЛЮЧЕНИЕ БИБЛИОТЕК И МОДУЛЕЙ <<<<< #
#==========================================================================================#

from pathlib import Path

#==========================================================================================#
# >>>>> РАЗМЕР ПОЛЬЗОВАТЕЛЬСКОЙ ДИРЕКТОРИИ <<<<< #
#==========================================================================================#

# Возвращает размер папки.
def SizeDirectory(folder):
    return ByteSize(sum(file.stat().st_size for file in Path(folder).rglob('*')))

#==========================================================================================#
# >>>>> ПРОВЕРКА НАЛИЧИЯ МЕСТА В КОЛЛЕКЦИИ <<<<< #
#==========================================================================================#

# Проверяет наличие места в коллекции.
def CheckSize(Bot, Message, UserID: str):
    # Создание пустого списка для сохранения размера коллекции.
    SizeList = list()

    # Список единиц измерения размера файлов. 
    Suffixes = ['B', 'KB', 'MB', 'PB' ]

    # Размер папки пользователя.
    Size = SizeDirectory(f'Data/Files/{UserID}')

    # Размер папки пользователя в виде строки и её разбивка.
    StrSize = str(Size).split(" ")

    # Добавление значений в список.
    for i in StrSize:
        SizeList.append(i)

    # Если единицы измерения папки 'GB', 'PB'.
    if SizeList[1] not in Suffixes:
        # Бот отправляет сообщение о ограничениях.
        Bot.send_message(Message.chat.id,
                          'Место для хранения ваших коллекций ограничено. Коллекционирование скоро завершится.'+ "\n" f'У вас осталось {round((2.00-float(SizeList[0])), 2)} ' + SizeList[1])

#==========================================================================================#
# >>>>> РАСЧЁТ РАЗМЕРА ДАННЫХ <<<<< #
#==========================================================================================#

class ByteSize(int):

    _KB = 1024
    _suffixes = 'B', 'KB', 'MB', 'GB', 'PB'

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.bytes = self.B = int(self)
        self.kilobytes = self.KB = self / self._KB**1
        self.megabytes = self.MB = self / self._KB**2
        self.gigabytes = self.GB = self / self._KB**3
        self.petabytes = self.PB = self / self._KB**4

        *suffixes, last = self._suffixes

        suffix = next((
            suffix
            for suffix in suffixes
            if 1 < getattr(self, suffix) < self._KB
        ), last)

        self.readable = suffix, getattr(self, suffix)

        super().__init__()


    def __str__(self):
        return self.__format__('.2f')


    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, super().__repr__())


    def __format__(self, format_spec):
        suffix, val = self.readable
        return '{val:{fmt}} {suf}'.format(val=val, fmt=format_spec, suf=suffix)


    def __sub__(self, other):
        return self.__class__(super().__sub__(other))


    def __add__(self, other):
        return self.__class__(super().__add__(other))
    

    def __mul__(self, other):
        return self.__class__(super().__mul__(other))


    def __rsub__(self, other):
        return self.__class__(super().__sub__(other))


    def __radd__(self, other):
        return self.__class__(super().__add__(other))
    
    
    def __rmul__(self, other):
        return self.__class__(super().__rmul__(other))    
