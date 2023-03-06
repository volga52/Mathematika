"""Файл содержит стандартные сообщения"""
from telegram_bot.setting.config import NUMBER, FRACTION


START_MESSAGE = "Привет!\nНапиши мне что нибудь\nИспользуй /help, чтобы " \
                "узнать список доступных команд! "

HELP_PREVIEW = 'Я могу ответить на следующие команды:'

UNKNOWN = 'Я не знаю, что с этим делать :astonished:'

MATICA_SALUTE = 'Matematica приветствует Тебя '

MATICA_PREVIEW = f"Чтобы ответить, чему равен 'x' вводи только"

number_mes_preview = f"цифры"
fraction_mes_preview = f"дробь.\nДробь вводится через знак /. Например '5/6'"
CANCEL_MES_PREVIEW = f"Чтобы выйти 'cancel' или '/cancel'"

DICT_MES_PREVIEW = {NUMBER: number_mes_preview, FRACTION: fraction_mes_preview}
