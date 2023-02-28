from telegram_bot.handlers.handler import Handler


class HandlerInline(Handler):
    """
    Класс обрабатывает входящие текстовые
    сообщения от нажатия на инлайн-кнопки
    """
    def __init__(self, dp):
        super().__init__(dp)

    def pressed_dtn(self):
        pass

    def handler(self):
        pass
