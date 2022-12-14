import telebot

from messages_handler import TeamExpenses
from utilities import get_token

TOKEN: str = get_token()
BOT = telebot.TeleBot(TOKEN, parse_mode=None)

HELP_COMMAND = """
/names Name1 Name2 ... - names to make clearing between\n
/payment Payer_Name Price Debtor1 Debtor2 ... - take payment into account.
\tPrice should be an integer or float value (e.g. 100 or 100.00)\n
/clearing_result - show result of clearing"""

NAMES_COMMAND_REGEX = r"/(\w+)(\s+\w+)+\s*$"
PAYMENT_COMMAND_REGEX = r"/(\w+\s+){2}\d+(.\d+)?(\s+\w+)+\s*$"
CLEARING_RESULT_COMMAND_REGEX = r"/\w+\s*$"

TEAMS: dict[str, TeamExpenses] = dict()


@BOT.message_handler(commands=['start', 'help'])
def send_welcome(message):
    BOT.reply_to(message, HELP_COMMAND)


@BOT.message_handler(commands=['names'], regexp=NAMES_COMMAND_REGEX)
def retrieve_names(message):
    new_team = TeamExpenses(message.chat.id)
    new_team.write_names(message.text)
    TEAMS.update({message.chat.id: new_team})
    BOT.reply_to(message, "Names are received")


@BOT.message_handler(commands=['payment'], regexp=PAYMENT_COMMAND_REGEX)
def load_payment(message):
    current_team = TEAMS.get(message.chat.id)
    try:
        if current_team is not None:
            current_team.write_payment(message.text)
            BOT.reply_to(message, "Payment is considered")
        else:
            BOT.reply_to(message, "Call command /names at first")
    except Exception as ex:
        BOT.reply_to(message, ex)


@BOT.message_handler(commands=['clearing_result'], regexp=CLEARING_RESULT_COMMAND_REGEX)
def show_clearing_result(message):
    current_team = TEAMS.get(message.chat.id)
    if current_team is not None:
        result = current_team.get_clearing_result()
        BOT.reply_to(message, result)
    else:
        BOT.reply_to(message, "Call command /names at first")


@BOT.message_handler(func=lambda m: True)
def echo_all(message):
    incorrect_command_message = "Your command is incorrect.\nPlease write one of these:"
    BOT.reply_to(message, incorrect_command_message + HELP_COMMAND)


BOT.infinity_polling()
