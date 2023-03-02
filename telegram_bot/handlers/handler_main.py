from telegram_bot.handlers.handler_com import HandlerCommands, HandlerEcho
from telegram_bot.handlers.handler_fsm import HandlerFSM


class HandlerMain:
    """Класс компоновщик"""
    def __init__(self, dp):
        self.dp = dp
        self.handler_commands = HandlerCommands(self.dp)
        self.handler_echo_end = HandlerEcho(self.dp)
        self.handler_fsm = HandlerFSM(self.dp)

    def handle(self):
        self.handler_commands.handler()
        self.handler_fsm.handler()

        # самый последний обработчик
        self.handler_echo_end.handler()
