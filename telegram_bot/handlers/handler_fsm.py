"""Обработчик машинного состояния"""
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types

from telegram_bot.FSM.equation_fsm import FSMEquation
from telegram_bot.handlers.handler import Handler


class HandlerFSM(Handler):
    """Класс обрабатывает машинное состояние """
    def __init__(self, dp):
        self.storage = MemoryStorage()
        super().__init__(dp=dp)
        self.dp.storage = self.storage
        self.gen = self.generator()

    async def process_setstate_command(self, message: types.Message):
        """Функция запускает первый этап машинного состояния"""
        await FSMEquation.first.set()
        await message.reply('start test', reply=False)

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
        await FSMEquation.next()
        await message.reply(f"First '{first}' argument", reply=False)

    async def excerpt_state_equation(self, message: types.Message,
                                     state: FSMContext):
        """Вывод фразы цитаты"""
        await FSMEquation.next()
        await message.reply("Excerpt", reply=False)

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

    def handler(self):
        self.dp.register_message_handler(self.process_setstate_command,
                                         state='*', commands=['startup'])
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
