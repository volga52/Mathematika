from aiogram import types
# from aiogram.types import InlineKeyboardButton

from telegram_bot.handlers.handler import Handler


class HandlerInline(Handler):
    """
    Класс обрабатывает входящие текстовые
    сообщения от нажатия на инлайн-кнопки
    """
    def __init__(self, dp):
        super().__init__(dp)
        self.task_cod = None

    async def pressed_btn(self, data):
        """Метод обработчик inline кнопок"""
        await self.dp.bot.answer_callback_query(data.id, 'press inline_button')
        await self.dp.bot.send_message(data.from_user.id,
                                       f'Нажата inline кнопка {data.data}')

    def handler(self):
        """Метод перехватывает нажатие на inline кнопки"""
        dp = self.dp

        @dp.callback_query_handler(lambda call: True)
        async def process_pressed_btn(call: types.CallbackQuery):
            await self.pressed_btn(call)

    # @staticmethod
    # def set_inline_btn_str(name_task: str):
    #     """Метод создает inline кнопку"""
    #     return InlineKeyboardButton(name_task, callback_data=name_task)
