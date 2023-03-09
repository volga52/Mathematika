from aiogram import Dispatcher
import logging

from telegram_bot.aphorisms.support_soul import Excerpt
import telegram_bot.logs.config.config_log
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
        # объект содержащий цитаты
        self.quantity_equations = 10
        self.excerpts = Excerpt()
        self.username = None
        # объект содержит элементы отображения для Bot-а
        self.message_dict = {'number_test': 0,
                             'equation': None,
                             'excerpt': None,
                             'answer': None}
        # экземпляр класса вычисляющего уравнение
        self.game = MathNumericalEquation()
        # Вид уравнений, тип математических элементов
        self.game.cod = cod
        # Изменение уровня сложности.
        # Возвращает сгенерированный список [min, max] значений
        self.gen_level_difficulty = None
        # Генератор создания уравнения. Возвращает сгенерированное уравнение
        self.generator_equations = None

    def launch(self, math_cod):
        """Запускает конструктор класса"""
        self.game.cod = math_cod
        self.excerpts.string_default = SLOGAN_APHORISM
        self.message_dict['excerpt'] = SLOGAN_APHORISM
        if self.game.cod == NUMBER:
            self.simple_equations()
        if self.game.cod == FRACTION:
            self.gen_level_difficulty = None
            self.generator_equations = None

    def fabric_simple_equations(self):
        """Создает и возвращает уравнение простые числа"""
        while True:
            # формируем сложность
            interval_values = next(self.gen_level_difficulty)
            self.game.min_ = interval_values[0]
            self.game.max_ = interval_values[1]

            equation: str = self.game.get_equation()
            right_answer = self.game.right_answer
            yield equation, right_answer

    def simple_equations(self):
        """
        Функция 'простые уравнения' запускает УЧЁБУ по уравнениям с одним
        неизвестным для целых чисел в выражении вида a+(b+c)=d
        :param quantity: количество уравнений
        """
        self.quantity_equations = NUMBER_SIMPLE_EQUATIONS
        # Изменение уровня сложности
        # возвращает генератор списка [min, max]
        self.gen_level_difficulty = self.chang_dif_gen_simple_equations()
        logger.info('Числовые уравнения. Запуск')
        # Утверждение фабрики уравнений
        self.generator_equations = self.fabric_simple_equations()

    def chang_dif_gen_simple_equations(self):
        """
        Функция генерирует значение интервала чисел в уравнении.
        Возвращает список [min, max]
        """
        # interval_values = [10, 20] default
        number = self.quantity_equations + 1
        interval_values = [VMIN_SE, VMAX_SE]
        for i in range(number):
            interval_values[0] += 3 * i
            interval_values[1] += 30 * i
            yield interval_values

    def get_main(self):
        equation, right_answer = next(self.generator_equations)
        # equation, right_answer = a
        self.message_dict['equation'] = equation
        self.message_dict['answer'] = right_answer
        # меняем номер уравнения
        self.message_dict['number_test'] += 1
        str_doc_num_test = f"Уравнение {self.message_dict.get('number_test')}"
        logger.info(str_doc_num_test)

        return equation


if __name__ == '__main__':
    b = MaticBotElem()
    # a = MaticBotElem('number')
    b.launch(NUMBER)
    print(b.excerpts())
    print(b.message_dict['number_test'])
    for i in range(15):
        print(b.get_main())
    print(b.message_dict['number_test'])
