from random import shuffle
import colorama
from pathlib import Path

# from telegram_bot.setting.config import SOUP_FILE, SLOGAN_APHORISM, BASE_DIR
from telegram_bot.setting.config import SOUP_FILE, SLOGAN_APHORISM


class Singleton(type):
    """
    Паттерн Singleton предоставляет механизм создания одного
    и только одного объекта класса,
    и предоставление к нему глобальную точку доступа.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class ExcerptOld(metaclass=Singleton):
    """
    Класс содержит и возвращает строки из файла (по умолчанию файл 'soul.txt')
    В дополнение, содержит функции вывода цветного шрифта
    """

    def __init__(self, file_name=SOUP_FILE):
        self.file_name = file_name
        self.excerpts = self.get_excerpt()
        self.string_default = 'Новое\n'
        colorama.init(autoreset=True)

    def __call__(self, *args, **kwargs):
        return self.get_new_excerpt

    @property
    def get_text(self):
        """Возвращает список строк файла"""
        path = Path(__file__).resolve().parent
        try:
            with open(f'{path}/{SOUP_FILE}', 'r', encoding='utf-8') \
                    as file_text:
                text_list = [line for line in file_text]
                shuffle(text_list)
        except FileNotFoundError:
            text_list = [SLOGAN_APHORISM for i in range(10)]
        return text_list

    @property
    def get_new_excerpt(self):
        """Возвращает одну строку из файла"""
        try:
            returned_string = next(self.excerpts)
        # Если афоризмы закончились перезапускаем класс
        except StopIteration:
            self.__init__()
            returned_string = self.string_default
        return returned_string

    def get_excerpt(self):
        """Функция организует поток строк."""
        for string in self.get_text:
            yield string

    @staticmethod
    def print_green_text(text):
        """Выводит текст зеленого цвета"""
        print(colorama.Fore.GREEN + text)
        # print(colorama.Style.RESET_ALL)

    @staticmethod
    def print_red_text(text):
        """Выводит текст красного цвета"""
        print(colorama.Fore.RED + text)
        # print(colorama.Style.RESET_ALL)
