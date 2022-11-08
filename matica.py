from time import sleep
import logging

import logs.config.config_log
from config import NUMBER_SIMPLE_EQUATIONS, NUMBER_CHECK_FRACTIONS, \
    LIST_OF_NEGATIVES, SLOGAN_APHORISM
from config import VALUE_MAX_FOR_SIMPLE_EQUATIONS_START as VMAX_SE
from config import VALUE_MIN_FOR_SIMPLE_EQUATIONS_START as VMIN_SE

from fractions_my_math import GenerationFractions
from equations import MathNumericalEquation
from support_soul import Excerpt


logger = logging.getLogger('math')
NUMBER = 'number'
FRACTION = 'fraction'


# class MathNumericalEquation:
#     """Класс создания уравнений. Их проверки"""
#
#     def __init__(self):
#         self.a = None
#         self.b = None
#         self.c = None
#         self.d = None
#         self.sign_first = ''
#         self.sign_second = ''
#         self.right_answer = None
#         self.min_ = 10
#         self.max_ = 20
#         self.cod = None
#         self.excerpts = Excerpt()
#         # Счетчик коэффициента вывода афоризма
#         self.count_not_correct_answer = 0
#         # Генератор элементов уравнения
#         self.gen_number = None
#
#     def set_values(self, cod):
#         """
#         Функция устанавливает значения 'a', 'b', 'c'
#         для выражения вида a+(b+c)=d
#         """
#         self.cod = cod
#         if self.cod == NUMBER:
#             self.a = self.generation_number()
#             self.b = self.generation_number()
#             self.d = self.generation_number()
#         if self.cod == FRACTION:
#             # Для дробей используем генератор дробей
#             gen_number = self.gen_number
#             gen_number.generation_fraction()
#             self.a = gen_number.a
#             self.b = gen_number.b
#             self.d = gen_number.d
#
#     def get_values(self):
#         """
#         Функция случайно расставляет математические знаки, вычисляет
#         значение c по известным a, b, d. для выражения вида a+(b+c)=d.
#         """
#         # Список математических знаков
#         list_operations = ['+', '-']
#
#         if self.d - self.a > 0:
#             self.sign_first = list_operations[0]
#             if self.b < self.d - self.a:
#                 self.c = self.d - self.a - self.b
#                 self.sign_second = list_operations[0]
#             else:
#                 self.c = self.b - self.d + self.a
#                 self.sign_second = list_operations[1]
#
#         else:
#             self.sign_first = list_operations[1]
#             if self.b < self.a - self.d:
#                 self.c = self.a - self.d - self.b
#                 self.sign_second = list_operations[0]
#             else:
#                 self.c = self.b - self.a + self.d
#                 self.sign_second = list_operations[1]
#
#         logger.info(f'Элементы выражения {self.a} {self.b} {self.c} {self.d}')
#
#     def create_rebus(self):
#         """
#         Функция составляет учебное уравнение и возвращает его в виде строки
#         Одно из чисел скрывается, случайным образом.
#         Его значение записывается в переменную 'answer'
#         """
#         # Список слагаемых для выражения a + (b + c) = d
#         terms_list = [self.d, self.a, self.b, self.c]
#         # Случайный выбор 'неизвестного' из a, b, c
#         unknown_position = random.randint(1, 3)
#         # Сохраняем правильный ответ
#         self.right_answer = terms_list[unknown_position]
#         # Заменяем значение 'неизвестного' на 'х'
#         terms_list[unknown_position] = 'x'
#
#         # Создаём строку учебного уравнения
#         equation_string = self.create_string(terms_list)
#
#         logger.info(f"Составлено уравнение '{equation_string}' "
#                     f'Ответ {self.right_answer}')
#         return equation_string
#
#     def create_string(self, list_param=None):
#         """
#         Функция составляет строку отображения уравнения вида a+(b+c)=d
#         Принимает список элементов выражения [d, a, b, c]
#         если списка нет подставляет элементы экземпляра класса
#         """
#         if not list_param:
#             terms_list = [self.d, self.a, self.b, self.c]
#         else:
#             terms_list = list_param
#
#         if isinstance(terms_list[3], int):
#             # Если 'с' число требуется его абсолютное значение, т.к.
#             # знаки арифметических действий определяются функцией 'get_values'
#             terms_list[3] = abs(self.c)
#
#         test_string = f'{terms_list[1]} {self.sign_first} ' \
#                       f'({terms_list[2]} {self.sign_second} {terms_list[3]})' \
#                       f' = {terms_list[0]}'
#         return test_string
#
#     def evaluation(self, test_string):
#         """
#         Функция показывает уравнение, просит ввести ответ и проверяет его.
#         Выводит общение в терминале
#         """
#         context = {
#             NUMBER: 'числом',
#             FRACTION: 'дробью',
#         }
#         # count_not_correct_answer = 0
#
#         while self.right_answer or self.right_answer == 0:
#             if self.count_not_correct_answer >= 19:
#                 # выводим афоризм зеленым шрифтом
#                 self.excerpts.print_green_text(self.excerpts())
#                 self.count_not_correct_answer = 0
#
#             print(test_string)
#             # Блок приема ответа
#
#             # Проверка типа ответа
#             try:
#                 if self.cod == NUMBER:
#                     answer = int(input('Введите ответ\nx = '))
#                 elif self.cod == FRACTION:
#                     first_answer = input('Введите ответ\nx = ')
#                     # # Получаем из ответа элементы дроби
#                     # response = GenerationFractions.crush(first_answer)
#                     # answer = Fraction(*response)
#                     # Актуальный и более простой вариант
#                     answer = Fraction(first_answer)
#             except ValueError:
#                 # print(format(f'Ответ должен быть {context[self.cod]}', '-^40'))
#                 text = format(f'Ответ должен быть {context[self.cod]}', '-^40')
#                 self.excerpts.print_red_text(text)
#                 self.count_not_correct_answer += 10
#                 continue
#
#             # Если тип верный проверяем 'ответ'
#             else:
#                 if answer == self.right_answer:
#                     print('Ответ верный')
#                     sleep(2)
#                     answer_for_log = 'Решено'
#                     # self.right_answer = None
#                     self.clear_all()
#                     self.count_not_correct_answer += 4
#                 else:
#                     self.count_not_correct_answer += 10
#
#                     answer_for_log = f'Не решено. Ввели {answer}'
#                     print('Не правильно. Попробуйте ещё\n')
#             logger.info(answer_for_log)
#
#     def eval_answer(self, answer):
#         """
#         Функция принимает ответ, оценивает его.
#         Возвращает оценку Да или Нет
#         """
#         return True if answer == self.right_answer else False
#
#     def clear_all(self):
#         """Функция обнуляет все значения"""
#         self.a = None
#         self.b = None
#         self.c = None
#         self.d = None
#         self.sign_first = ''
#         self.sign_second = ''
#         self.right_answer = None
#
#     def generation_number(self):
#         """
#         Функция генерирует случайное целое число в диапазоне i_min : i_max
#         """
#         return random.randint(self.min_, self.max_)
#
#     @staticmethod
#     def reactions_str(eval_answer):
#         """Функция выводит ответ 'Верно' или 'Не верно'"""
#         return YES if eval_answer else NO
#
#     def run(self):
#         """Функция запускает процесс 'решения уравнений' """
#         # Создаем выражение a+(b+c)=d
#         # self.set_values('number')
#         self.set_values(self.cod)
#         self.get_values()
#         # Составляем уравнение
#         finish_string = self.create_rebus()
#         # Отображаем уравнение. Ввод и проверка ответа
#         self.evaluation(finish_string)


def simple_equations(quantity=5):
    """
    Функция 'простые уравнения' запускает УЧЁБУ по уравнениям с одним
    неизвестным для целых чисел в выражении вида a+(b+c)=d
    :param quantity: количество уравнений
    """
    logger.info('Числовые уравнения. Запуск')
    game = MathNumericalEquation()
    game.cod = NUMBER
    # Изменение уровня сложности
    # возвращает генератор списка [min, max]
    level_difficulty = changing_dif_gen(quantity)

    for i in range(quantity):
        interval_values = next(level_difficulty)
        print(f'\n*** Уравнение {i + 1}')

        logger.info(f'Уравнение {i + 1}')

        game.min_ = interval_values[0]
        game.max_ = interval_values[1]
        game.run()


def changing_dif_gen(number=5):
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


def check_fractions(number=5):
    """
    Функция запускает УЧЁБУ по уравнениям с одним неизвестным
    для ДРОБЕЙ в выражении вида a+(b+c)=d
    :param number: - количество проходов
    """
    logger.info('Запущен генератор уравнения с дробями')

    game = MathNumericalEquation()
    game.cod = FRACTION

    # Создаем экземпляр класса - генератора дробей
    game.gen_number = GenerationFractions()
    # Меняем уровень сложности
    # Генератор уровня сложности
    level_difficulty = GenerationFractions.start_changing_difficulty_level()

    for i in range(number):
        # Устанавливаем уровень сложности
        game.gen_number.difficulty_level = next(level_difficulty)

        print(f'\n*** Уравнение {i + 1}')
        game.run()


def target_is_denial(string):
    """Проверка строки на наличие отрицания выполнять упражнение"""
    # non_list = ['не', 'no', "don't"]
    string.lower()
    answer = False
    for i in LIST_OF_NEGATIVES:
        if string.find(i) > -1:
            answer = True
            break
    return answer


def fraction_with_integer(number=5):
    pass


def main():
    """Функция запуска программы математического тренажера"""
    excerpts = Excerpt()
    excerpts.string_default = SLOGAN_APHORISM

    user_name = input('Привет! Как тебя зовут? Набери: ')
    # Вывод первоначального лозунга
    excerpts.print_green_text(excerpts.string_default)

    print('Какие уравнения будем решать?')
    while True:
        answer = input('с числами - введите 1\nс дробями - введите 2'
                       '\nВыход q\nТвое решение? ')
        # Учеба 'уравнения с числами'
        if answer == '1':
            # simple_equations(10)
            simple_equations(NUMBER_SIMPLE_EQUATIONS)
        # Учеба 'уравнения с дробями'
        elif answer == '2':
            check_fractions(NUMBER_CHECK_FRACTIONS)
        # Учеба 'Дроби с целыми числами'
        elif answer == '3':
            pass
        # Выход из программы
        elif answer == 'q':
            print('Пока!')
            sleep(1)
            break
        # Проверка строки на наличие отрицания выполнять упражнение
        elif target_is_denial(answer):
            # выводим афоризм зеленым шрифтом
            excerpts.print_green_text(excerpts())
            sleep(2)
            continue
        else:
            print(f'\n{user_name} Давай все-таки порешаем уравнения\n')
            continue
        print(f'Все решено. {user_name}, ты молодец! \n')
        sleep(2)
        print('Еще будем решать?')


if __name__ == '__main__':
    main()
