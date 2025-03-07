from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReactionTypeEmoji
import requests

API_TOKEN = '7740967401:AAHtUCvRkHzCYoq0gVD0C6Zi-lTFLRekVao'
bot = TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    if text.startswith('اینستا') or text.startswith('insta'):
        url = text.split(' ')[1]
        api_url = f'https://haji.kavir-host-sub2.ir//api/insta.php?url={url}'
        response = requests.get(api_url)
        if response.status_code == 200:
            media_url = response.json().get('media')
            bot.send_message(message.chat.id, media_url, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "خطایی در دریافت اطلاعات از اینستاگرام رخ داد.")
    
    elif text.startswith('یوتیوب'):
        url = text.split(' ')[1]
        api_url = f'https://api.api4dev.ir/yt/download?url={url}'
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            video_url = data.get('tunneled_link')
            title = data.get('title')
            bot.send_message(message.chat.id, f"عنوان: {title}\nلینک: {video_url}", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "خطایی در دریافت اطلاعات از یوتیوب رخ داد.")
    
    elif text.startswith('تیک تاک'):
        url = text.split(' ')[1]
        api_url = f'https://api.api4dev.ir/tiktok?url={url}'
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            # فرض می‌کنیم لینک ویدیو در کلید 'video_url' قرار دارد
            video_url = data.get('video_url', 'لینک ویدیو یافت نشد')
            bot.send_message(message.chat.id, video_url, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "خطایی در دریافت اطلاعات از تیک تاک رخ داد.")
    
    elif text.startswith('هوش'):
        query = ' '.join(text.split(' ')[1:])
        api_url = f"https://api4dev.ir/ai/saveai/black.php?userid={message.from_user.id}&Model=gpt-4o&text={requests.utils.quote(query)}"
        response = requests.get(api_url)
        if response.status_code == 200:
            ai_response = response.json().get('response')
            bot.send_message(message.chat.id, ai_response, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "خطایی در دریافت پاسخ از هوش مصنوعی رخ داد.")
    
    else:
        bot.send_message(message.chat.id, "دستور شناخته نشد. لطفاً از دستورات معتبر استفاده کنید.")

bot.infinity_polling()
