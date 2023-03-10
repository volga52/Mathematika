"""Обработчик машинного состояния"""
from asyncio import sleep

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types

from telegram_bot.FSM.equation_fsm import FSMEquation
from telegram_bot.handlers.handler import Handler
from telegram_bot.setting.config import DICT_TASK
from telegram_bot.setting.messages import MATICA_PREVIEW, DICT_MES_PREVIEW, \
    CANCEL_MES_PREVIEW, FIRST_EXC_ANSWER


class HandlerFSM(Handler):
    """Класс обрабатывает машинное состояние """

    def __init__(self, dp):
        self.storage = MemoryStorage()
        super().__init__(dp=dp)
        self.dp.storage = self.storage

        # self.gen = self.generator()
        self.gen = None
        self.math_cod = None

    async def process_tasks_command(self, message: types.Message, state: FSMContext):
        """Устанавливает тип уравнений. Запускает FSM состояние"""
        await message.answer('OK', reply_markup=self.markup.remove_menu())
        # Получение ответа с кнопки
        cod = message.text.split('_')[1]
        self.math_cod = DICT_TASK[cod]

        # Инициация элемента математики
        # По окончании требуется очистка

        # a = await self.math_init()
        # await self.bot.send_message(message.from_user.id, a)

        await self.set_state(message, state)

    async def set_state(self, message: types.Message, state: FSMContext):
        """Функция запускает первый этап машинного состояния"""
        text_rules = f"{MATICA_PREVIEW} {DICT_MES_PREVIEW[self.math_cod]}" \
                     f"\n'Набери число и жми ВВОД (ENTER)'" \
                     f"\n{CANCEL_MES_PREVIEW}"
        await self.bot.send_message(message.from_user.id,
                                    FIRST_EXC_ANSWER[0],
                                    reply_markup=self.markup.remove_menu())
        await self.bot.send_message(message.from_user.id, text_rules)
        await FSMEquation.first.set()
        # state = FSMEquation.states[0]
        await self.first_state_equation(message, state)

    async def math_init(self):
        """Метод запускает создание математических выражений"""
        self.dp.math_element.launch(self.math_cod)
        quantity_test = self.dp.math_element.quantity_equations
        self.gen = self.generator(quantity_test)

    async def first_state_equation(self, message: types.Message,
                                   state: FSMContext):
        """Обработка первого запроса машинного состояния"""
        await self.math_init()
        self.dp.math_element.message_dict['answer'] = FIRST_EXC_ANSWER[1]
        print(self.dp.math_element.message_dict)

        await self.bot.send_message(message.from_user.id, f'first_start')
        await FSMEquation.test.set()

    async def excerpt_state_equation(self, message: types.Message,
                                     state: FSMContext):
        """Вывод фразы цитаты"""
        await message.answer(f'Получено {message.text}')

        await sleep(1)
        text = self.dp.math_element.message_dict.get('excerpt', 'None')
        await message.reply(f'{text}', reply=False)
        # Реакция на правильность ответа
        if message.text == 'Yes':
            pass
        else:
            pass
        await FSMEquation.next()
        await self.new_equation(message, state)

    async def test_state_equation(self, message: types.Message, state: FSMContext):
        """Обработка-работа с уравнениями"""
        await FSMEquation.excerpt.set()
        await message.answer('Test')
        if int(message.text) == self.dp.math_element.message_dict['answer']:
            await message.reply('Верно')
            message.text = 'Yes'
        else:
            await message.reply('Не правильно')
            message.text = 'No'
        await self.excerpt_state_equation(message, state)

    async def new_equation(self, message: types.Message, state: FSMContext):
        if message.text == 'Yes':
            try:
                gen = next(self.gen)
                await message.reply(f"Test {gen} ", reply=False)
                # Получение нового уравнения
                text_equation = self.dp.math_element.get_main()
                value_dict = self.dp.math_element.message_dict
                print(text_equation, 'get_math_value', value_dict)

            except StopIteration:
                await message.reply('Finish!!!')
                await FSMEquation.last.set()
                await self.last_state_equation(message, state)
                return

        await message.reply(
                self.dp.math_element.message_dict.get('equation', 'None'))
        await FSMEquation.next()

    async def last_state_equation(self, message: types.Message,
                                  state: FSMContext):
        """Завершение машинного состояния"""
        await message.reply("Last", reply=False)
        await state.finish()

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
        self.dp.register_message_handler(self.new_equation,
                                         state=FSMEquation.equation)
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
