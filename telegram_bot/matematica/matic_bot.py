from aiogram import Dispatcher
import logging

# from telegram_bot.aphorisms.support_soul import Excerpt
import telegram_bot.logs.config.config_log
# from telegram_bot.matematica.equations import MathNumericalEquation
from telegram_bot.matematica.equations_new import MathNumericalEquation

from telegram_bot.setting.config import SLOGAN_APHORISM, NUMBER, FRACTION
from telegram_bot.setting.config import NUMBER_SIMPLE_EQUATIONS, \
    NUMBER_CHECK_FRACTIONS, LIST_OF_NEGATIVES, SLOGAN_APHORISM
from telegram_bot.setting.config import \
    VALUE_MAX_FOR_SIMPLE_EQUATIONS_START as VMAX_SE
from telegram_bot.setting.config import \
    VALUE_MIN_FOR_SIMPLE_EQUATIONS_START as VMIN_SE

logger = logging.getLogger('matic')


class MaticBotElem:
    """Класс оперирует уравнениями"""
    def __init__(self, cod=None):
        # self.dp = dp
        # self.excerpts = Excerpt()
        # self.excerpts.string_default = SLOGAN_APHORISM
        self.username = None
        # Вид уравнений, действие
        self.cod = cod
        self.message_dict = {'number_test': 0,
                             'equations': None,
                             'excerpts': None,
                             'answer': None}

    def main(self, cod):
        # Определяемся с видом уравнения или выход
        self.cod = cod
        if self.cod == NUMBER:
            self.message_dict['equations'] = self.simple_equations()
        elif self.cod == FRACTION:
            pass

    def simple_equations(self, quantity=5):
        """
        Функция 'простые уравнения' запускает УЧЁБУ по уравнениям с одним
        неизвестным для целых чисел в выражении вида a+(b+c)=d
        :param quantity: количество уравнений
        """
        logger.info('Числовые уравнения. Запуск')
        game = MathNumericalEquation()
        game.cod = self.cod
        # Изменение уровня сложности
        # возвращает генератор списка [min, max]
        level_difficulty = self.changing_dif_gen(quantity)
        # for i in range(quantity):
        #     interval_values = next(level_difficulty)
        #     logger.info(f'Уравнение {i + 1}')
        #     self.message_dict.get('number_test')

        # Проверка работоспособности
        interval_values = next(level_difficulty)
        # система нумерации уравнений
        # __меняем номер уравнения
        self.message_dict['number_test'] += 1
        number_test = f"Уравнение {self.message_dict.get('number_test')}"
        logger.info(number_test)

        game.min_ = interval_values[0]
        game.max_ = interval_values[1]
        return game.get_equation

    def changing_dif_gen(self, number=5):
        """
        Функция генерирует значение интервала чисел в уравнении.
        Возвращает список [min, max]
        """
        # interval_values = [10, 20] default
        interval_values = [VMIN_SE, VMAX_SE]
        for i in range(number):
            interval_values[0] += 3 * i
            interval_values[1] += 30 * i
            yield interval_values
