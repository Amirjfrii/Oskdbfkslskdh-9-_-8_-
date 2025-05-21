from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReactionTypeEmoji
import time
import requests

bot = TeleBot(token="2200135262:AAHRzxyl09pbKwK7t1-KiRToZthzG8wuCNg/test")


@bot.business_message_handler(func=lambda message: True)
def echo_message(message):
    api_url = f"https://api.pamickweb.ir/api/chat.php?apikey=u2aog60LOEX77965161495973057fxyl&text={message.text}&userid={message.chat.id}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        api_output = response.text
        bot.send_message(message.chat.id, api_output, business_connection_id=message.business_connection_id, parse_mode='Markdown')
    except requests.exceptions.RequestException as e:
        bot.send_message(message.chat.id, f"Error: {e}", business_connection_id=message.business_connection_id)








bot.infinity_polling()

