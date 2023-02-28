from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, InlineKeyboardButton


class Keyboards:
    """
    Класс Keyboards предназначен для создания разметки интерфейса бота
    """
    def __init__(self):
        self.markup = None
        self.DB = None

    def menu_on_start(self):
        """Стартовая клавиатура"""
        button_01 = KeyboardButton('/matematica')
        button_02 = KeyboardButton('/Описание')
        button_03 = KeyboardButton('/help')

        self.markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                          one_time_keyboard=True)
        self.markup.add(button_01).add(button_02).add(button_03)

        return self.markup

    def menu_on_pressed_startup(self):
        """Инлайн клавиатура для команды matematica"""
        # btn_1 = KeyboardButton('/startup')
        btn_1 = KeyboardButton('/начать')
        btn_2 = KeyboardButton('other')

        self.markup = ReplyKeyboardMarkup(True, True, row_width=3)
        self.markup.add(btn_1).insert(btn_2)

        return self.markup

    @staticmethod
    def set_inline_btn(value):
        """
        Создает и возвращает инлайн-кнопку по входным параметрам
        """
        return InlineKeyboardButton(str(value), callback_data=str(value.name))

    @staticmethod
    def remove_menu():
        """
        Удаляет кнопки из меню и возвращает пустое меню
        """
        return ReplyKeyboardRemove()

