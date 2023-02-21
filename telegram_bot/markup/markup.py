from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove


class Keyboards:
    """
    Класс Keyboards предназначен для создания разметки интерфейса бота
    """
    def __init__(self):
        self.markup = None
        self.DB = None

    def menu_on_start(self):
        """Стартовая клавиатура"""
        button_01 = KeyboardButton('/test')
        button_02 = KeyboardButton('/Описание')
        button_03 = KeyboardButton('/help')

        self.markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                          one_time_keyboard=True)
        self.markup.add(button_01).add(button_02).add(button_03)

        return self.markup


