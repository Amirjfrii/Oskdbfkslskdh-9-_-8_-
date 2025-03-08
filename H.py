import os
from telethon import TelegramClient, events, Button
from pytubefix import YouTube

# تنظیمات Telethon
API_ID = '22051826'
API_HASH = '713ee0c13c60e46ecf2f9c3af4a7694b'
BOT_TOKEN = '7729006326:AAHFgany1VpIVigtdAL7x5IvDjYwJ5eWpkA'  # جایگزین کنید با توکن ربات خود از @BotFather

# ایجاد کلاینت Telethon
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

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
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("سلام! لینک ویدئوی یوتیوب را برای من بفرستید تا آن را دانلود کنم.")

# دریافت لینک ویدئو از کاربر
@client.on(events.NewMessage)
async def handle_video_link(event):
    chat_id = event.chat_id
    video_url = event.text

    # بررسی اینکه آیا لینک معتبر است
    if "youtube.com" not in video_url and "youtu.be" not in video_url:
        await event.respond("لطفاً یک لینک معتبر یوتیوب ارسال کنید.")
        return

    # دریافت کیفیت‌های ویدئو
    qualities = get_video_qualities(video_url)
    if not qualities:
        await event.respond("خطا در دریافت کیفیت‌های ویدئو. لطفاً لینک را بررسی کنید.")
        return

    # ایجاد دکمه‌های شیشه‌ای برای کیفیت‌ها
    buttons = []
    for quality, itag in qualities:
        buttons.append([Button.inline(quality, data=f"quality:{itag}:{video_url}")])

    await event.respond("لطفاً کیفیت ویدئو را انتخاب کنید:", buttons=buttons)

# مدیریت انتخاب کیفیت توسط کاربر
@client.on(events.CallbackQuery)
async def handle_quality_selection(event):
    data = event.data.decode('utf-8')
    if data.startswith("quality:"):
        _, itag, video_url = data.split(":")
        itag = int(itag)

        # دانلود ویدئو با کیفیت انتخاب شده
        await event.respond("در حال دانلود ویدئو... لطفاً منتظر بمانید.")
        video_path = download_video(video_url, itag)

        if video_path:
            try:
                # ارسال ویدئو به کاربر
                await client.send_file(event.chat_id, video_path)
                await event.respond("ویدئو با موفقیت ارسال شد!")
            except Exception as e:
                await event.respond(f"خطا در ارسال ویدئو: {e}")
            finally:
                # حذف فایل موقت
                if os.path.exists(video_path):
                    os.remove(video_path)
        else:
            await event.respond("خطا در دانلود ویدئو. لطفاً لینک را بررسی کنید.")

# اجرای ربات
if __name__ == "__main__":
    # ایجاد پوشه downloads اگر وجود نداشته باشد
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    print("ربات در حال اجرا است...")
    client.run_until_disconnected()
