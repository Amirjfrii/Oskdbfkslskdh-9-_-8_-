import telebot
import requests
import json

# توکن و اطلاعات ربات
bot_token = "7740967401:AAGsPE7IuNyPJFZD3c92Q9yIBnW95BrmptE"
channel_id = "sellnumchannel"
bot_username = "gptjafarbot"  # بدون @
bot = telebot.TeleBot(bot_token)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text
    user_id = message.from_user.id
    message_id = message.message_id

    if text == "/start":
        welcome_message = (
            "سلام کاربر عزیز! 🌟\n\n"
            "به دنیای شگفت‌انگیز ربات ما خوش آمدید! 🗣️ شما می‌توانید با وارد کردن پیام‌های خود، از امکانات بی‌نظیر ما بهره‌مند شوید.\n\n"
            "✨ چه کارهایی می‌توانم برای شما انجام دهم؟ ✨\n"
            "- 🔍 یافتن پاسخ‌ها به سوالات شما\n"
            "- 📚 نوشتن مقالات علمی و تخصصی\n"
            "- 💻 نوشتن کدهای برنامه‌نویسی برای پروژه‌های شما\n"
            "- 👩‍💻 نوشتن ایمیل‌ها و نامه‌ها به صورت حرفه‌ای\n"
            "- 🌎 ترجمه به هر زبانی که نیاز دارید\n"
            "- 📷 تولید عکس\n"
            "- 🗣 ساخت ویس\n\n"
            "امیدواریم لحظات خوبی را با ما سپری کنید!"
        )
        reply_markup = telebot.types.InlineKeyboardMarkup()
        reply_markup.add(
            telebot.types.InlineKeyboardButton("اضافه کردن به گروه ✨", url=f"https://t.me/{bot_username}?startgroup=new"),
            telebot.types.InlineKeyboardButton("ساخت عکس 📷", callback_data="generate_photo"),
            telebot.types.InlineKeyboardButton("🤖 Chat GPT", callback_data="chat_gpt"),
            telebot.types.InlineKeyboardButton("ساخت ویس 🗣", callback_data="generate_voice"),
            telebot.types.InlineKeyboardButton("📣Channel", url=f"https://t.me/{channel_id}")
        )
        bot.send_message(chat_id, welcome_message, reply_markup=reply_markup)

    elif text.startswith("/gpt"):
        query = text[5:]
        api_response = requests.get(f"https://api4dev.ir/ai/saveai/black.php?userid={user_id}&Model=gpt-4o&text={query}").text
        bot.send_message(chat_id, api_response, reply_to_message_id=message_id)

    elif text.startswith("/ai"):
        query = text[4:]
        api_response = requests.get(f"https://ExDi.ir/photo/image?prompt={query}&model=flux-pro&height=740&width=1024&enhance=true").json()
        if api_response['code'] == 200:
            photo_url = api_response['image']
            bot.send_photo(chat_id, photo_url, reply_to_message_id=message_id)
        else:
            bot.send_message(chat_id, "❌ مشکلی در تولید عکس به وجود آمد.", reply_to_message_id=message_id)

    elif text.startswith("/male"):
        query = text[6:]
        api_response = requests.get(f"https://api-free.ir/api/voice.php?text={query}&mod=FaridNeural").json()
        if api_response['ok'] and api_response['code'] == 200:
            audio_url = api_response['result']
            bot.send_audio(chat_id, audio_url, reply_to_message_id=message_id)
        else:
            bot.send_message(chat_id, "❌ مشکلی در تولید ویس صدای مرد به وجود آمد.", reply_to_message_id=message_id)

    elif text.startswith("/female"):
        query = text[8:]
        api_response = requests.get(f"https://api-free.ir/api/voice.php?text={query}&mod=DilaraNeural").json()
        if api_response['ok'] and api_response['code'] == 200:
            audio_url = api_response['result']
            bot.send_audio(chat_id, audio_url, reply_to_message_id=message_id)
        else:
            bot.send_message(chat_id, "❌ مشکلی در تولید ویس صدای زن به وجود آمد.", reply_to_message_id=message_id)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    callback_data = call.data
    callback_chat_id = call.message.chat.id
    callback_id = call.id

    if callback_data == "chat_gpt":
        bot.answer_callback_query(callback_id, "لطفا برای پرسش و پاسخ از دستور /gpt استفاده کنید.\nبرای مثال: /gpt ایران کجاست")

    elif callback_data == "generate_photo":
        bot.answer_callback_query(callback_id, "لطفا با دستور /ai برای تولید عکس استفاده کنید.\nبرای مثال: /ai ربات قرمز")
    elif callback_data == "generate_voice":
        bot.answer_callback_query(callback_id, "برای ساخت ویس صدای مرد دستور /male و برای صدای زن دستور /female استفاده کنید.\nبرای مثال: /male ربات مارکار کریتور")

# شروع ربات
bot.polling()
