import telebot
import requests
import os

# توکن ربات تلگرام شما
TOKEN = '7740967401:AAHtUCvRkHzCYoq0gVD0C6Zi-lTFLRekVao'
bot = telebot.TeleBot(TOKEN)

# تابع برای دانلود فایل از لینک
def download_file(url, file_name):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return True
    return False

# دستور start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! به ربات همه‌کاره خوش آمدید. 🚀\n\n"
                          "دستورات موجود:\n"
                          "1. دانلود از اینستاگرام: ارسال لینک با عبارت `insta` قبل از آن.\n"
                          "2. دانلود از یوتیوب: ارسال لینک با عبارت `youtube` قبل از آن.\n"
                          "3. دانلود از تیک‌تاک: ارسال لینک با عبارت `tiktok` قبل از آن.\n"
                          "4. هوش مصنوعی: ارسال متن با عبارت `هوش` قبل از آن.\n\n"
                          "مثال:\n"
                          "insta https://www.instagram.com/p/example\n"
                          "هوش سلام چطوری؟")

# اینستاگرام دانلودر
@bot.message_handler(func=lambda message: message.text.startswith('insta'))
def handle_instagram(message):
    try:
        url = message.text.split(' ')[1]  # جدا کردن لینک از دستور
        api_url = f"https://mr-amiri.ir/api/instagram?url={url}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            
            # استخراج لینک از ساختار خروجی
            if isinstance(data, list) and len(data) > 0:
                media_info = data[0]  # اولین عنصر لیست
                media_url = media_info.get('media')  # استخراج لینک از کلید 'media'
            else:
                bot.reply_to(message, "خطا: ساختار خروجی API نامعتبر است. 😢")
                return
            
            if media_url:
                # دانلود فایل
                file_name = "instagram_video.mp4"
                if download_file(media_url, file_name):
                    # ارسال فایل به کاربر
                    with open(file_name, 'rb') as file:
                        bot.send_video(message.chat.id, file)
                    os.remove(file_name)  # حذف فایل پس از ارسال
                else:
                    bot.reply_to(message, "خطا در دانلود فایل. 😢")
            else:
                bot.reply_to(message, "لینک دانلود یافت نشد. 😢")
        else:
            bot.reply_to(message, "خطا در ارتباط با سرور. لطفا دوباره تلاش کنید.")
    except Exception as e:
        bot.reply_to(message, f"خطا: {e}")
# یوتیوب دانلودر
@bot.message_handler(func=lambda message: message.text.startswith('youtube'))
def handle_youtube(message):
    try:
        url = message.text.split(' ')[1]  # جدا کردن لینک از دستور
        api_url = f"https://api.api4dev.ir/yt/download?url={url}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            video_url = data.get('tunneled_link')
            title = data.get('title')
            if video_url:
                # دانلود فایل
                file_name = "youtube_video.mp4"
                if download_file(video_url, file_name):
                    # ارسال فایل به کاربر
                    with open(file_name, 'rb') as file:
                        bot.send_video(message.chat.id, file, caption=title)
                    os.remove(file_name)  # حذف فایل پس از ارسال
                else:
                    bot.reply_to(message, "خطا در دانلود فایل. 😢")
            else:
                bot.reply_to(message, "لینک دانلود یافت نشد. 😢")
        else:
            bot.reply_to(message, "خطا در ارتباط با سرور. لطفا دوباره تلاش کنید.")
    except Exception as e:
        bot.reply_to(message, f"خطا: {e}")

# تیک‌تاک دانلودر
@bot.message_handler(func=lambda message: message.text.startswith('tiktok'))
def handle_tiktok(message):
    try:
        url = message.text.split(' ')[1]  # جدا کردن لینک از دستور
        api_url = f"https://api.api4dev.ir/tiktok?url={url}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            # فرض کنید لینک دانلود در کلید `download_url` قرار دارد
            download_url = data.get('download_url')
            if download_url:
                # دانلود فایل
                file_name = "tiktok_video.mp4"
                if download_file(download_url, file_name):
                    # ارسال فایل به کاربر
                    with open(file_name, 'rb') as file:
                        bot.send_video(message.chat.id, file)
                    os.remove(file_name)  # حذف فایل پس از ارسال
                else:
                    bot.reply_to(message, "خطا در دانلود فایل. 😢")
            else:
                bot.reply_to(message, "لینک دانلود یافت نشد. 😢")
        else:
            bot.reply_to(message, "خطا در ارتباط با سرور. لطفا دوباره تلاش کنید.")
    except Exception as e:
        bot.reply_to(message, f"خطا: {e}")

# هوش مصنوعی
@bot.message_handler(func=lambda message: message.text.startswith('هوش'))
def handle_ai(message):
    try:
        text = message.text.replace('هوش', '').strip()  # حذف کلمه "هوش" از متن
        sender_id = message.from_user.id  # آیدی کاربر
        api_url = f"backupapi.s6.viptelbot.top/advancedai/save?sender={sender_id}&text={text}"
        response = requests.get(api_url)
        if response.status_code == 200:
            bot.reply_to(message, response.text)  # ارسال پاسخ هوش مصنوعی
        else:
            bot.reply_to(message, "خطا در ارتباط با سرور هوش مصنوعی. لطفا دوباره تلاش کنید.")
    except Exception as e:
        bot.reply_to(message, f"خطا: {e}")

# شروع ربات
print("ربات فعال شد! 🤖")
bot.polling()
