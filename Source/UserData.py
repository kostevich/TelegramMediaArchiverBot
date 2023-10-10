from dublib.Methods import ReadJSON, WriteJSON
from telebot import types

import os

# Описательная структура пользователя.
class UserData:

	# Создаёт нового пользователя.
	def __CreateUser(self):
		# Создание экземпляра пользователя.
		self.__User = {
			"chat-id": None,
			"premium": False
		}
		# Создание папки файлов пользователя.
		os.makedirs("Data/Files/" + self.__UserID)
		# Создание папки архивов пользователя.
		os.makedirs("Data/Archives/" + self.__UserID)
		# Сохранение файла пользователя.
		self.save()

	# Конструктор.
	def __init__(self, UserID: str):

		#---> Генерация статических свойств.
		#==========================================================================================#
		# ID пользователя.
		self.__UserID = str(UserID)
		# Данные пользователя.
		self.__User = None

		#---> Инициализация пользователя.
		#==========================================================================================#
		# Список названий файлов в директории пользователя.
		Files = list()
		# Получение списка файлов в директории.
		Files = os.listdir("Data/Users")
		# Фильтрация только файлов формата JSON.
		Files = list(filter(lambda x: x.endswith(".json"), Files))

		# Если пользователя не существует.
		if self.__UserID + ".json" not in Files:
			self.__CreateUser()

		# Иначе читаем данные пользователя.
		else:
			self.__User = ReadJSON("Data/Users/" + self.__UserID + ".json")

	# Возвращает ID пользователя.
	def getUserID(self) -> str:
		return self.__UserID

	# Сохраняет данные пользователя.
	def save(self):
		# Сохранение файла пользователя.
		WriteJSON("Data/Users/" + self.__UserID + ".json", self.__User)