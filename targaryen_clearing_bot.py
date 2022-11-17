from typing import Set

import telebot

from messages_handler import TeamExpenses
from utilities import get_token

TOKEN: str = get_token()
BOT = telebot.TeleBot(TOKEN, parse_mode=None)

HELP_COMMAND = """
/names Name1 Name2 ... - names to make clearing between\n
/payment Payer_Name Price Debtor1 Debtor2 ... - take payment into account"""

TEAMS: Set[TeamExpenses] = set()


@BOT.message_handler(commands=['start', 'help'])
def send_welcome(message):
    BOT.reply_to(message, HELP_COMMAND)


@BOT.message_handler(commands=['names'])
def retrieve_names(message):
    new_team = TeamExpenses(message.chat.id)
    new_team.write_names(message.text)
    TEAMS.add(new_team)
    BOT.reply_to(message, "Names are received")


@BOT.message_handler(commands=['payment'])
def load_payment(message):
    current_team = next((team for team in TEAMS if team.user_id == message.chat.id), None)
    if current_team is not None:
        current_team.write_payment(message.text)
        BOT.reply_to(message, "Payment is considered")
    else:
        BOT.reply_to(message, "Call command /names at first")


@BOT.message_handler(commands=['clearing_result'])
def show_clearing_result(message):
    current_team = next((team for team in TEAMS if team.user_id == message.chat.id), None)
    if current_team is not None:
        result = current_team.get_clearing_result()
        BOT.reply_to(message, result)
    else:
        BOT.reply_to(message, "Call command /names at first")


@BOT.message_handler(func=lambda m: True)
def echo_all(message):
    BOT.reply_to(message, message.text)


BOT.infinity_polling()
