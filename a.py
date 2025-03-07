from telethon import TelegramClient, events
import requests
import os

# تنظیمات توکن ربات
bot_token = 'YOUR_BOT_TOKEN'  # توکن ربات خود را اینجا وارد کنید

# تنظیمات API های شما
INSTA_API = "https://mr-amiri.ir/api/instagram?url="
YOUTUBE_API = "https://api.api4dev.ir/yt/download?url="
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

# ایجاد کلاینت Telethon با توکن ربات
client = TelegramClient('bot_session', api_id=None, api_hash=None).start(bot_token=bot_token)

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
            api_url = YOUTUBE_API + url
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                video_url = data.get('tunneled_link')
                title = data.get('title')
                if video_url:
                    file_name = "youtube_video.mp4"
                    if download_file(video_url, file_name):
                        await client.send_file(event.chat_id, file_name, caption=title)
                        os.remove(file_name)
                    else:
                        await event.reply("خطا در دانلود فایل. 😢")
                else:
                    await event.reply("لینک دانلود یافت نشد. 😢")
            else:
                await event.reply("خطا در ارتباط با سرور. لطفا دوباره تلاش کنید.")

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
                             "هوش سلام چطوری؟")

    except Exception as e:
        await event.reply(f"خطا: {e}")

# شروع ربات
print("ربات فعال شد! 🤖")
with client:
    client.run_until_disconnected()
