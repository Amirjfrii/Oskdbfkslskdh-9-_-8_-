from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReactionTypeEmoji
import time
import requests

bot = TeleBot(token="5000351662:AAF2ZXY9mJ-R19uPhCAuU1MuxYWXJvlm8iU/test")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    api_url = f"http://backupapi.s6.viptelbot.top/advancedai/save?sender={message.chat.id}&text={message.text}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        api_output = response.text
        bot.send_message(message.chat.id, api_output, parse_mode='Markdown')
    except requests.exceptions.RequestException as e:
        bot.send_message(message.chat.id, f"Error: {e}")


@bot.message_handler(commands=['start'])
def start(m):
  bot.reply_to(m, 'hi send your message plz')





bot.infinity_polling()
