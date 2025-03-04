from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReactionTypeEmoji
import time
import requests

bot = TeleBot(token="2200135262:AAG8Ar9ag6GJPFq9QfRZ7QnvRL1cm9JbIhE/test")


@bot.business_message_handler(func=lambda message: True)
def echo_message(message):
    api_url = f"https://open.wiki-api.ir/apis-1/ChatGPT-4o?q={message.text}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        api_output = response.json().get('results')
        bot.send_message(message.chat.id, api_output, business_connection_id=message.business_connection_id)
    except requests.exceptions.RequestException as e:
        bot.send_message(message.chat.id, f"Error: {e}", business_connection_id=message.business_connection_id)








bot.polling()
