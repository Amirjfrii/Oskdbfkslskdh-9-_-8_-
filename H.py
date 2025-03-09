import os
import telebot
from pytubefix import YouTube

# تنظیمات Telebot
BOT_TOKEN = '7729006326:AAHFgany1VpIVigtdAL7x5IvDjYwJ5eWpkA'  # جایگزین کنید با توکن ربات خود از @BotFather

# ایجاد کلاینت Telebot
bot = telebot.TeleBot(BOT_TOKEN)

# تابع برای دریافت بالاترین کیفیت ویدئو
def get_highest_quality(url: str):
    try:
        yt = YouTube(url)
        # دریافت بالاترین کیفیت progressive (هم ویدئو و هم صدا)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        return stream
    except Exception as e:
        print(f"خطا در دریافت کیفیت‌ها: {e}")
        return None

# تابع برای دانلود ویدئو با بالاترین کیفیت
def download_video(url: str) -> str:
    try:
        yt = YouTube(url)
        # دریافت بالاترین کیفیت progressive
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video_path = stream.download(output_path='downloads')
        return video_path
    except Exception as e:
        print(f"خطا در دانلود ویدئو: {e}")
        return None

# دستور /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سلام! لینک ویدئوی یوتیوب را برای من بفرستید تا آن را دانلود کنم.")

# دریافت لینک ویدئو از کاربر
@bot.message_handler(func=lambda message: True)
def handle_video_link(message):
    chat_id = message.chat.id
    video_url = message.text

    # بررسی اینکه آیا لینک معتبر است
    if "youtube.com" not in video_url and "youtu.be" not in video_url:
        bot.reply_to(message, "لطفاً یک لینک معتبر یوتیوب ارسال کنید.")
        return

    # دریافت بالاترین کیفیت ویدئو
    stream = get_highest_quality(video_url)
    if not stream:
        bot.reply_to(message, "خطا در دریافت کیفیت‌های ویدئو. لطفاً لینک را بررسی کنید.")
        return

    # دانلود ویدئو با بالاترین کیفیت
    bot.reply_to(message, "در حال دانلود ویدئو... لطفاً منتظر بمانید.")
    video_path = download_video(video_url)

    if video_path:
        try:
            # ارسال ویدئو به کاربر
            with open(video_path, 'rb') as video_file:
                bot.send_video(chat_id, video_file)
            bot.reply_to(message, "ویدئو با موفقیت ارسال شد!")
        except Exception as e:
            bot.reply_to(message, f"خطا در ارسال ویدئو: {e}")
        finally:
            # حذف فایل موقت
            if os.path.exists(video_path):
                os.remove(video_path)
    else:
        bot.reply_to(message, "خطا در دانلود ویدئو. لطفاً لینک را بررسی کنید.")

# اجرای ربات
if __name__ == "__main__":
    # ایجاد پوشه downloads اگر وجود نداشته باشد
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    print("ربات در حال اجرا است...")
    bot.polling(none_stop=True)
