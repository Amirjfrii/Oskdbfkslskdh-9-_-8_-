from telethon import TelegramClient, events, Button
from pytubefix import YouTube
import os
import requests

# تنظیمات API تلگرام
api_id = 'YOUR_API_ID'  # از my.telegram.org دریافت کنید
api_hash = 'YOUR_API_HASH'  # از my.telegram.org دریافت کنید
bot_token = 'YOUR_BOT_TOKEN'  # توکن ربات شما

# تنظیمات API های شما (برای اینستاگرام و تیک‌تاک)
INSTA_API = "https://mr-amiri.ir/api/instagram?url="
TIKTOK_API = "https://api.api4dev.ir/tiktok?url="
AI_API = "https://backupapi.s6.viptelbot.top/advancedai/save?sender={}&text={}"

# تابع برای دانلود فایل از لینک
def download_file(url, file_name):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return True
    return False

# تابع برای دریافت کیفیت‌های موجود یوتیوب
def get_youtube_qualities(url):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension='mp4')
        qualities = []
        for stream in streams:
            resolution = stream.resolution
            itag = stream.itag
            qualities.append((resolution, itag))
        return yt.title, qualities
    except Exception as e:
        print(f"خطا: {e}")
        return None, []

# تابع برای دانلود ویدیو یوتیوب با کیفیت انتخاب‌شده
def download_youtube_video(url, itag, output_path="."):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_by_itag(itag)
        file_name = stream.default_filename
        stream.download(output_path)
        return file_name
    except Exception as e:
        print(f"خطا در دانلود ویدیو: {e}")
        return None

# ایجاد کلاینت Telethon
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# رویداد دریافت پیام
@client.on(events.NewMessage)
async def handle_message(event):
    try:
        text = event.text
        sender_id = event.sender_id

        # اینستاگرام دانلودر
        if text.startswith('insta'):
            url = text.split(' ')[1]
            api_url = INSTA_API + url
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    media_url = data[0].get('media')
                    if media_url:
                        file_name = "instagram_video.mp4"
                        if download_file(media_url, file_name):
                            await client.send_file(event.chat_id, file_name)
                            os.remove(file_name)
                        else:
                            await event.reply("خطا در دانلود فایل. 😢")
                    else:
                        await event.reply("لینک دانلود یافت نشد. 😢")
                else:
                    await event.reply("خطا: ساختار خروجی API نامعتبر است. 😢")
            else:
                await event.reply("خطا در ارتباط با سرور. لطفا دوباره تلاش کنید.")

        # یوتیوب دانلودر
        elif text.startswith('youtube'):
            url = text.split(' ')[1]
            title, qualities = get_youtube_qualities(url)
            if not qualities:
                await event.reply("خطا در دریافت کیفیت‌های ویدیو. لطفاً لینک را بررسی کنید. 😢")
                return
            
            # ایجاد دکمه‌های شیشه‌ای برای کیفیت‌ها
            buttons = []
            for resolution, itag in qualities:
                buttons.append([Button.inline(resolution, data=f"yt:{itag}:{url}")])
            
            await event.reply(f"کیفیت‌های موجود برای ویدیو: {title}\nلطفاً یک کیفیت انتخاب کنید:", buttons=buttons)

        # تیک‌تاک دانلودر
        elif text.startswith('tiktok'):
            url = text.split(' ')[1]
            api_url = TIKTOK_API + url
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                download_url = data.get('download_url')
                if download_url:
                    file_name = "tiktok_video.mp4"
                    if download_file(download_url, file_name):
                        await client.send_file(event.chat_id, file_name)
                        os.remove(file_name)
                    else:
                        await event.reply("خطا در دانلود فایل. 😢")
                else:
                    await event.reply("لینک دانلود یافت نشد. 😢")
            else:
                await event.reply("خطا در ارتباط با سرور. لطفا دوباره تلاش کنید.")

        # هوش مصنوعی
        elif text.startswith('هوش'):
            user_text = text.replace('هوش', '').strip()
            api_url = AI_API.format(sender_id, user_text)
            response = requests.get(api_url)
            if response.status_code == 200:
                await event.reply(response.text)
            else:
                await event.reply("خطا در ارتباط با سرور هوش مصنوعی. لطفا دوباره تلاش کنید.")

        # دستور start
        elif text == '/start':
            await event.reply("سلام! به ربات همه‌کاره خوش آمدید. 🚀\n\n"
                             "دستورات موجود:\n"
                             "1. دانلود از اینستاگرام: ارسال لینک با عبارت `insta` قبل از آن.\n"
                             "2. دانلود از یوتیوب: ارسال لینک با عبارت `youtube` قبل از آن.\n"
                             "3. دانلود از تیک‌تاک: ارسال لینک با عبارت `tiktok` قبل از آن.\n"
                             "4. هوش مصنوعی: ارسال متن با عبارت `هوش` قبل از آن.\n\n"
                             "مثال:\n"
                             "insta https://www.instagram.com/p/example\n"
                             "youtube https://www.youtube.com/watch?v=example\n"
                             "هوش سلام چطوری؟")

    except Exception as e:
        await event.reply(f"خطا: {e}")

# رویداد کلیک روی دکمه‌های شیشه‌ای
@client.on(events.CallbackQuery)
async def handle_callback(event):
    try:
        data = event.data.decode('utf-8')
        if data.startswith('yt:'):
            _, itag, url = data.split(':')
            await event.edit("در حال دانلود ویدیو... لطفاً منتظر بمانید. ⏳")
            
            # دانلود ویدیو
            file_name = download_youtube_video(url, int(itag))
            if file_name:
                # ارسال ویدیو به کاربر
                await client.send_file(event.chat_id, file_name)
                os.remove(file_name)
            else:
                await event.edit("خطا در دانلود ویدیو. لطفاً دوباره تلاش کنید. 😢")
    except Exception as e:
        await event.edit(f"خطا: {e}")

# شروع ربات
print("ربات فعال شد! 🤖")
with client:
    client.run_until_disconnected()
