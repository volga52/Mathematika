from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

NUMBER = 'number'
FRACTION = 'fractions'

list_task = (NUMBER, FRACTION)


class Keyboards:
    """
    Класс Keyboards предназначен для создания разметки интерфейса бота
    """
    def __init__(self):
        self.markup = None
        self.DB = None

    def menu_on_start(self):
        """Создает и возвращает стартовую клавиатуру"""
        button_01 = KeyboardButton('/matematica')
        button_02 = KeyboardButton('/Описание')
        button_03 = KeyboardButton('/help')

        self.markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                          one_time_keyboard=True)
        self.markup.add(button_01).add(button_02).add(button_03)

        return self.markup

    def menu_on_pressed_startup(self):
        """Создает и возвращает клавиатуру для команды matematica"""
        # btn_1 = KeyboardButton('/startup')
        btn_1 = KeyboardButton('/начать')
        btn_2 = KeyboardButton('other')

        self.markup = ReplyKeyboardMarkup(True, True, row_width=3)
        self.markup.add(btn_1).insert(btn_2)

        return self.markup

    def set_task(self):
        """Создаёт и возвращает клавиатуру для определения вида задания"""
        btn_1 = KeyboardButton('/простые_числа')
        btn_2 = KeyboardButton('/просто_дроби')

        self.markup = ReplyKeyboardMarkup(True, True, is_persistent=True)
        self.markup.insert(btn_1).insert(btn_2)

        return self.markup

    def tasks_inline_kb(self):
        """Создает и возвращает inline клавиатуру: выбор типа задания"""
        self.markup = InlineKeyboardMarkup(row_width=2)
        for names_btn in list_task:
            button_inline = self.set_inline_btn_str(names_btn)
            # self.markup.add(button_inline)
            self.markup.insert(button_inline)
        return self.markup

    @staticmethod
    def set_inline_btn_str(value: str):
        """
        Создает и возвращает inline-кнопку по входному параметру-строке
        """
        return InlineKeyboardButton(value, callback_data=value)

    @staticmethod
    def remove_menu():
        """
        Удаляет кнопки из меню и возвращает пустое меню
        """
        return ReplyKeyboardRemove()
