"""Обработчик машинного состояния"""
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types

from telegram_bot.FSM.equation_fsm import FSMEquation
from telegram_bot.handlers.handler import Handler
from telegram_bot.setting.config import DICT_TASK
from telegram_bot.setting.messages import MATICA_PREVIEW, DICT_MES_PREVIEW, \
    CANCEL_MES_PREVIEW


class HandlerFSM(Handler):
    """Класс обрабатывает машинное состояние """
    def __init__(self, dp):
        self.storage = MemoryStorage()
        super().__init__(dp=dp)
        self.dp.storage = self.storage

        self.gen = self.generator()
        self.math_cod = None

    async def set_state(self, message: types.Message):
        """Функция запускает первый этап машинного состояния"""
        await FSMEquation.first.set()
        text_rules = f"{MATICA_PREVIEW} {DICT_MES_PREVIEW[self.math_cod]}" \
               f"\n{CANCEL_MES_PREVIEW}"
        await self.bot.send_message(message.from_user.id, text_rules,
                                    reply_markup=self.markup.remove_menu())

    async def process_tasks_command(self, message: types.Message):
        """Устанавливает тип уравнений. Запускает FSM состояние"""
        await message.answer('OK', reply_markup=self.markup.remove_menu())
        # Получение ответа с кнопки
        cod = message.text.split('_')[1]
        self.math_cod = DICT_TASK[cod]

        # Инициация элемента математики
        # По окончании требуется очистка

        # a = await self.math_init()
        # await self.bot.send_message(message.from_user.id, a)

        await self.set_state(message)

    async def math_init(self):
        """Метод запускает создание математических выражений"""
        self.dp.math_element.launch(self.math_cod)

    async def get_math_value(self):
        """Метод получает и возвращает математическое выражение"""
        next(self.gen)
        text_equation = self.dp.math_element.get_main()
        print(text_equation, 'get_math_value')
        return text_equation

    async def process_cancel_equation(self, message: types.Message,
                                      state: FSMContext):
        """
        Отмена-выход из машинного состояния через команду или ключевое слово
        """
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Выход из FSM')

    async def first_state_equation(self, message: types.Message,
                                   state: FSMContext):
        """Обработка первого запроса машинного состояния"""
        async with state.proxy() as data:
            first = message.text
            data['first'] = first

        await self.bot.send_message(message.from_user.id, 'first_start')
        await FSMEquation.next()
        await self.api_fsm(message)
        # await message.reply(f"First '{first}' argument", reply=False)

    async def excerpt_state_equation(self, message: types.Message,):
        """Вывод фразы цитаты"""
        await FSMEquation.next()
        await message.reply("Excerpt", reply=False)
        text_equation = self.dp.math_element.message_dict.get('equation',
                                                              'None')
        await message.answer(text_equation)

    async def test_state_equation(self, message: types.Message,
                                  state: FSMContext):
        """Обработка-работа с уравнениями"""
        try:
            gen = next(self.gen)
            await message.reply(f"Test {gen} ", reply=False)

        except StopIteration:
            await message.reply('Finish!!!')
            await FSMEquation.next()

    async def last_state_equation(self, message: types.Message,
                                  state: FSMContext):
        """Завершение машинного состояния"""
        await message.reply("Last", reply=False)

        await state.finish()

    async def api_fsm(self, message: types.Message):
        """Управление элементами FSM машины"""
        # Если генератора нет инициируем math
        if self.dp.math_element.message_dict.get('number_test') == 0:
            # первое уравнение
            # first_ex = await self.math_init()
            await self.math_init()
            first_ex = await self.get_math_value()
            message.text = first_ex
            answer = self.dp.math_element.message_dict.get('answer')
            print(first_ex, 'Ответ', type(answer), str(answer))
            # print(first_ex)
            await self.bot.send_message(message.from_user.id, 'math_start')
            await self.excerpt_state_equation(message)
        else:
            pass

    def handler(self):
        self.dp.register_message_handler(
            self.process_tasks_command,
            state='*',
            commands=['простые_числа', 'просто_дроби'])

        self.dp.register_message_handler(self.process_cancel_equation,
                                         state='*', commands=['cancel'])
        self.dp.register_message_handler(self.process_cancel_equation, Text(
            equals=['cancel', 'выход'], ignore_case=True), state='*')
        self.dp.register_message_handler(self.first_state_equation,
                                         state=FSMEquation.first)
        self.dp.register_message_handler(self.excerpt_state_equation,
                                         state=FSMEquation.excerpt)
        self.dp.register_message_handler(self.test_state_equation,
                                         state=FSMEquation.test)
        self.dp.register_message_handler(self.last_state_equation,
                                         state=FSMEquation.last)

    @staticmethod
    def generator(number: int = 5):
        """Генератор порядкового номера тренировочного уравнения"""
        for i in range(number):
            print(f'Next {i}')
            yield i + 1
