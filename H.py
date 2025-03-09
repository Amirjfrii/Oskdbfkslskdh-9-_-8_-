import os
import telebot
from pytubefix import YouTube

# تنظیمات Telebot
BOT_TOKEN = '7729006326:AAHFgany1VpIVigtdAL7x5IvDjYwJ5eWpkA'  # جایگزین کنید با توکن ربات خود از @BotFather

# ایجاد کلاینت Telebot
bot = telebot.TeleBot(BOT_TOKEN)

# تابع برای دریافت کیفیت‌های ویدئو
def get_video_qualities(url: str):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension='mp4')
        qualities = [(stream.resolution, stream.itag) for stream in streams]
        return qualities
    except Exception as e:
        print(f"خطا در دریافت کیفیت‌ها: {e}")
        return None

# تابع برای دانلود ویدئو با کیفیت مشخص
def download_video(url: str, itag: int) -> str:
    try:
        yt = YouTube(url)
        video = yt.streams.get_by_itag(itag)
        video_path = video.download(output_path='downloads')
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

    # دریافت کیفیت‌های ویدئو
    qualities = get_video_qualities(video_url)
    if not qualities:
        bot.reply_to(message, "خطا در دریافت کیفیت‌های ویدئو. لطفاً لینک را بررسی کنید.")
        return

    # ایجاد دکمه‌های شیشه‌ای برای کیفیت‌ها
    markup = telebot.types.InlineKeyboardMarkup()
    for quality, itag in qualities:
        markup.add(telebot.types.InlineKeyboardButton(text=quality, callback_data=f"quality:{itag}:{video_url}"))

    bot.send_message(chat_id, "لطفاً کیفیت ویدئو را انتخاب کنید:", reply_markup=markup)

# مدیریت انتخاب کیفیت توسط کاربر
@bot.callback_query_handler(func=lambda call: True)
def handle_quality_selection(call):
    data = call.data
    if data.startswith("quality:"):
        _, itag, video_url = data.split(":")
        itag = int(itag)

        # دانلود ویدئو با کیفیت انتخاب شده
        bot.answer_callback_query(call.id, "در حال دانلود ویدئو... لطفاً منتظر بمانید.")
        video_path = download_video(video_url, itag)

        if video_path:
            try:
                # ارسال ویدئو به کاربر
                with open(video_path, 'rb') as video_file:
                    bot.send_video(call.message.chat.id, video_file)
                bot.send_message(call.message.chat.id, "ویدئو با موفقیت ارسال شد!")
            except Exception as e:
                bot.send_message(call.message.chat.id, f"خطا در ارسال ویدئو: {e}")
            finally:
                # حذف فایل موقت
                if os.path.exists(video_path):
                    os.remove(video_path)
        else:
            bot.send_message(call.message.chat.id, "خطا در دانلود ویدئو. لطفاً لینک را بررسی کنید.")

# اجرای ربات
if __name__ == "__main__":
    # ایجاد پوشه downloads اگر وجود نداشته باشد
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    print("ربات در حال اجرا است...")
    bot.polling(none_stop=True)
