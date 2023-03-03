# import asyncio
from aiogram import types
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode, ContentType
from emoji import emojize

from telegram_bot.FSM.equation_fsm import FSMEquation
from telegram_bot.handlers.handler import Handler
from telegram_bot.setting.messages import *


class HandlerCommands(Handler):
    """
    Класс обрабатывает основные входящие команды (/start, /help)
    """
    def __init__(self, dispatcher):
        super().__init__(dispatcher)

    async def process_start_command(self, message: types.Message):
        await message.reply(START_MESSAGE,
                            reply_markup=self.markup.menu_on_start())

    async def process_help_command(self, message: types.Message):
        msg = text(bold(HELP_PREVIEW), *HELP_COM_LIST, sep='\n')
        await message.reply(msg, parse_mode=ParseMode.MARKDOWN_V2)

    async def process_matematica_command(self, message: types.Message):
        txt = f'{message.from_user.first_name}! {MATICA_SALUTE}'
        # await message.reply(txt)
        await message.answer(txt, reply_markup=self.markup.remove_menu())
        await message.answer(
            'Начать?', reply_markup=self.markup.menu_on_pressed_startup())

    # Команда '/начать'
    async def process_startup_command(self, message: types.Message):
        await message.answer('OK', reply_markup=self.markup.remove_menu())
        self.dp.math_element.main()
        text_eq = self.dp.math_element.message_dict.get('equations')
        await self.bot.send_message(message.from_user.id, text_eq)

    async def process_fsm_command(self, message: types.Message):
        await message.answer('Inline_choice', reply_markup=self.markup.tasks_inline_kb())

    def handler(self):
        self.dp.register_message_handler(self.process_start_command,
                                         commands=['start'])
        self.dp.register_message_handler(self.process_help_command,
                                         commands=['help'])
        self.dp.register_message_handler(self.process_matematica_command,
                                         commands=['matematica'])
        # self.dp.register_message_handler(self.process_startup_command,
        #                                  commands=['startup'])
        self.dp.register_message_handler(self.process_startup_command,
                                         commands=['начать'])
        self.dp.register_message_handler(self.process_fsm_command,
                                         commands=['choice'])


class HandlerEcho(Handler):
    """
    Класс возвращает неизвестные команды и просто неизвестную информацию
    """
    def __init__(self, dispatcher):
        super().__init__(dispatcher)

    async def echo_message(self, msg: types.Message):
        await self.bot.send_message(msg.from_user.id, msg.text)

    async def unknown_message(self, msg: types.Message):
        message_text = text(emojize(UNKNOWN), italic('\nЯ просто напомню,'),
                            'что есть', code('команда'), '/help')
        await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN_V2)

    def handler(self):
        # Самая последняя регистрация
        self.dp.register_message_handler(self.echo_message)
        self.dp.register_message_handler(self.unknown_message,
                                         content_types=ContentType.ANY)

    @staticmethod
    def check_is_digit(value):
        if value.isdigit():
            pass
