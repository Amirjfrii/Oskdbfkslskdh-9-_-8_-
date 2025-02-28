#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# ┌──────────────────────────────────────┐
# │                                   │
# │   > installing guide :               │
# │      $ pip install pyrogram==2.0.41  │
# │      $ pip install asyncio           │
# └──────────────────────────────────────┘

import os, random, asyncio, time
from pyrogram import Client, filters, errors
from pyrogram.raw import functions, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


#           ---         ---         ---         #
api_id = 23703937 # main api id from my.telegram.org/apps
api_hash = '779a983cfcccef536bbfd5ec66deb627' # main api hash from my.telegram.org/apps
bot_token = '2200260147:AAFGYLlq8nIhQEzK3jqBThTB-yVpq2Gn9MY' # main bot token from @botFather
bot_admins = [1495973057, 2200903945] # admin userID
#           ---         ---         ---         #
sleeping = 2 # main sleep time in sec ***[DO NOT EDIT]***
step = None # current step ***[DO NOT EDIT]***
tempClient = dict() # temporary client holder ***[DO NOT EDIT]***
isWorking = list() # Temporary Active Eval Names ***[DO NOT EDIT]***
#           ---         ---         ---         #


if not os.path.isdir('sessions') :
    os.mkdir('sessions')


if not os.path.isfile('app.txt') :
    with open('app.txt', 'w', encoding='utf-8') as file:
        file.write(str(api_id) + ' ' + api_hash)


async def randomString() -> str:
    '''Return a random string'''
    size = random.randint(4, 8)
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVLXYZ') for _ in range(size))


async def randomAPP():
    with open('app.txt', 'r', encoding='utf-8') as file:
        file = file.read().split('\n')
        app_id, app_hash = random.choice(file).split()
    return app_id, app_hash


async def accountList() :
    return [myFile.split('.')[0] for myFile in os.listdir('sessions') if os.path.isfile(os.path.join('sessions', myFile))]


async def remainTime(TS):
    TS = time.time() - TS
    if TS < 60 :
        return str(int(TS)) + ' ثانیه'
    else :
        min = int(TS/60)
        sec = TS%60
        return str(int(min)) + ' دقیقه و ' + str(int(sec)) + ' ثانیه'


bot = Client(
    "LampStack",
    bot_token = bot_token,
    api_id = api_id,
    api_hash = api_hash,
    test_mode=True
)


try :
    os.system("clear")
except :
    os.system("cls")
print('Bot is Running ...')


#           StartCommand            #
@bot.on_message(filters.command(['start', 'cancel']) & filters.private & filters.user(bot_admins))
async def StartResponse(client, message):
    global step, tempClient, isWorking
    try:
        tempClient['client'].disconnect()
    except:
        pass
    tempClient = {}
    step = None
    my_keyboard = [
        [InlineKeyboardButton('افزودن اکانت ➕', callback_data='addAccount'), InlineKeyboardButton('✖️ حذف اکانت', callback_data='removeAccount')],
        [InlineKeyboardButton('عملیات عضویت ⚪️', callback_data='joinEval'), InlineKeyboardButton('⚪️ عملیات لفت', callback_data='leftEval')],
        [InlineKeyboardButton('عملیات ویو پست ⚫️', callback_data='viewEval'), InlineKeyboardButton('⚫️ عملیات ری اکشن پست', callback_data='reActionEval')],
        [InlineKeyboardButton('عملیات نظرسنجی 🔴', callback_data='voteEval'), InlineKeyboardButton('🔴 عملیات ریپورت پست', callback_data='reportPostPublic')],
        [InlineKeyboardButton('🟡 عملیات بلاک کاربر 🟡', callback_data='blockEval')],
        [InlineKeyboardButton('لیست اکانت ها 📊', callback_data='accountsList'), InlineKeyboardButton('♻️ بررسی اکانت ها', callback_data='checkAccounts')],
        [InlineKeyboardButton('تنظیم زمان 🕠', callback_data='setTime'), InlineKeyboardButton('📛 لغو تمام عملیات ها', callback_data='endAllEvals')],
    ]
    await message.reply('<b>> به منوی اصلی خوش آمدید :</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)

#           StopEval            #
@bot.on_message(filters.regex('^/stop_\w+') & filters.private & filters.user(bot_admins))
async def StopEval(client, message):
    global step, isWorking
    my_keyboard = [
        [InlineKeyboardButton('🔙', callback_data='backToMenu')],
    ]
    evalID = message.text.replace('/stop_', '')
    if evalID in isWorking:
        isWorking.remove(evalID)
        await message.reply(f'<b>عملیات با شناسه {evalID} با موفقیت خاتمه یافت ✅</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
    else:
        await message.reply(f'<b>عملیات موردنظر یافت نشد !</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)



#           callback query            #
@bot.on_callback_query()
async def callbackQueries(client, query):
    global step, bot_admins, tempClient, isWorking, sleeping
    chat_id = query.message.chat.id
    message_id = query.message.id
    data = query.data
    query_id = query.id
    if chat_id in bot_admins:
        if data == 'backToMenu':
            try:
                tempClient['client'].disconnect()
            except:
                pass
            tempClient = {}
            step = None
            my_keyboard = [
                [InlineKeyboardButton('افزودن اکانت ➕', callback_data='addAccount'), InlineKeyboardButton('✖️ حذف اکانت', callback_data='removeAccount')],
                [InlineKeyboardButton('عملیات عضویت ⚪️', callback_data='joinEval'), InlineKeyboardButton('⚪️ عملیات لفت', callback_data='leftEval')],
                [InlineKeyboardButton('عملیات ویو پست ⚫️', callback_data='viewEval'), InlineKeyboardButton('⚫️ عملیات ری اکشن پست', callback_data='reActionEval')],
                [InlineKeyboardButton('عملیات نظرسنجی 🔴', callback_data='voteEval'), InlineKeyboardButton('🔴 عملیات ریپورت پست', callback_data='reportPostPublic')],
                [InlineKeyboardButton('🟡 عملیات بلاک کاربر 🟡', callback_data='blockEval')],
                [InlineKeyboardButton('لیست اکانت ها 📊', callback_data='accountsList'), InlineKeyboardButton('♻️ بررسی اکانت ها', callback_data='checkAccounts')],
                [InlineKeyboardButton('تنظیم زمان 🕠', callback_data='setTime'), InlineKeyboardButton('📛 لغو تمام عملیات ها', callback_data='endAllEvals')],
            ]
            await bot.edit_message_text(chat_id, message_id, '<b>> به منوی اصلی خوش آمدید :</b>', reply_markup=InlineKeyboardMarkup(my_keyboard))

        elif data == 'endAllEvals':
            step = None
            evalsCount = len(isWorking)
            isWorking = list()
            await bot.invoke(functions.messages.SetBotCallbackAnswer(query_id=int(query_id), cache_time=1, alert=True, message=f'تمام {evalsCount} عملیات فعال با موفقیت متوقف شدند ✅'))

        elif data == 'addAccount':
            step = 'getPhoneForLogin'
            my_keyboard = [
                [InlineKeyboardButton('🔙', callback_data='backToMenu')],
            ]
            await bot.edit_message_text(chat_id, message_id, '<b>- برای افزودن اکانت لطفا شماره مورد نظرتان را ارسال نمایید :</b>', reply_markup=InlineKeyboardMarkup(my_keyboard))
        
        elif data == 'removeAccount':
            step = 'removeAccount'
            my_keyboard = [
                [InlineKeyboardButton('🔙', callback_data='backToMenu')],
            ]
            await bot.edit_message_text(chat_id, message_id, '<b>- برای حذف اکانت لطفا شماره مورد نظرتان را ارسال نمایید :</b>', reply_markup=InlineKeyboardMarkup(my_keyboard))

        elif data == 'accountsList':
            if os.path.isfile(f'./accounts.txt'):
                os.unlink(f'./accounts.txt')
            myLen = len((await accountList()))
            if myLen == 0 :
                await bot.invoke(functions.messages.SetBotCallbackAnswer(query_id=int(query_id), cache_time=1, alert=True, message='اکانتی یافت نشد !'))
            else:
                with open(f'./accounts.txt', 'w') as my_file:
                    my_file.write("\n".join(await accountList()))
                try:
                    await bot.send_document(chat_id, f'./accounts.txt', caption=f'تعداد کل اکانت ها : {myLen}')
                    os.unlink(f'./accounts.txt')
                except:
                    pass

        elif data == 'checkAccounts':
            if len(await accountList()) == 0 :
                await bot.invoke(functions.messages.SetBotCallbackAnswer(query_id=int(query_id), cache_time=1, alert=True, message='اکانتی یافت نشد ❗️'))
            else:
                evalID = await randomString()
                isWorking.append(evalID)
                deleted = 0
                error = 0
                free = 0
                cli = None
                TS = time.time()
                AllCount = len(await accountList())
                await bot.edit_message_text(chat_id, message_id, '<b>عملیات بررسی اکانت ها شروع شد ...</b>')
                for session in ((await accountList())):
                    if evalID not in isWorking:
                        break
                    try:
                        await cli.disconnect()
                    except:
                        pass
                    await asyncio.sleep(sleeping)
                    try:
                        api_id2, api_hash2 = await randomAPP()
                        cli = Client(f'sessions/{session}', api_id2, api_hash2)
                        await cli.connect()
                        await cli.resolve_peer("@durov")
                        await cli.disconnect()
                    except (errors.SessionRevoked, errors.UserDeactivated, errors.AuthKeyUnregistered, errors.UserDeactivatedBan, errors.Unauthorized):
                        try:
                            await cli.disconnect()
                        except:
                            pass
                        os.unlink(f'sessions/{session}.session')
                        deleted += 1
                    except Exception as e:
                        try:
                            await cli.disconnect()
                        except:
                            pass
                        error += 1
                    else:
                        free += 1
                    finally:
                        spendTime = await remainTime(TS)
                        allChecked = deleted + free + error
                        await bot.edit_message_text(chat_id, message_id, f'''♻️ عملیات بررسی اکانت های ربات ...

• کل اکانت ها : {AllCount}
• اکانت های بررسی شده : {allChecked}
• اکانت های سالم : {free}
• سشن های خراب : {deleted}
• خطاهای ناشناخته : {error}
• زمان سپری شده : {spendTime}

برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
                try:
                    isWorking.remove(evalID)
                except:
                    pass
                allChecked = deleted + free + error
                spendTime = await remainTime(TS)
                my_keyboard = [
                    [InlineKeyboardButton('🔙', callback_data='backToMenu')],
                ]
                await bot.send_message(chat_id, f'''عملیات بررسی اکانت ها با موفقیت به اتمام رسید ✅

• کل اکانت ها : {AllCount}
• اکانت های بررسی شده : {allChecked}
• اکانت های سالم : {free}
• سشن های خراب : {deleted}
• خطاهای ناشناخته : {error}
• زمان سپری شده : {spendTime}''', reply_markup=InlineKeyboardMarkup(my_keyboard))


        elif data == 'setTime':
            step = 'setTime'
            my_keyboard = [
                [InlineKeyboardButton('🔙', callback_data='backToMenu')],
            ]
            await bot.edit_message_text(chat_id, message_id, f'<b>فاصله زمانی فعلی {sleeping} ثانیه میباشد\nدرصورتیکه قصد تغییر فاصله زمانی بین انجام عملیات ها را دارید عدد جدید را ارسال نمایید :</b>', reply_markup=InlineKeyboardMarkup(my_keyboard))

        elif data == 'joinEval':
            if len(await accountList()) == 0 :
                await bot.invoke(functions.messages.SetBotCallbackAnswer(query_id=int(query_id), cache_time=1, alert=True, message='اکانتی یافت نشد ❗️'))
            else:
                step = 'joinAccounts'
                my_keyboard = [
                    [InlineKeyboardButton('🔙', callback_data='backToMenu')],
                ]
                await bot.edit_message_text(chat_id, message_id, '<b>- برای عملیات عضویت لطفا یوزرنیم یا لینک خصوصی مورد نظرتان را ارسال کنید :</b>', reply_markup=InlineKeyboardMarkup(my_keyboard))

        elif data == 'leftEval':
            if len(await accountList()) == 0 :
                await bot.invoke(functions.messages.SetBotCallbackAnswer(query_id=int(query_id), cache_time=1, alert=True, message='اکانتی یافت نشد ❗️'))
            else:
                step = 'leaveAccounts'
                my_keyboard = [
                    [InlineKeyboardButton('🔙', callback_data='backToMenu')],
                ]
                await bot.edit_message_text(chat_id, message_id, '<b>- برای عملیات لفت لطفا شناسه عددی مورد نظرتان را ارسال کنید :</b>', reply_markup=InlineKeyboardMarkup(my_keyboard))

        elif data == 'viewEval':
            if len(await accountList()) == 0 :
                await bot.invoke(functions.messages.SetBotCallbackAnswer(query_id=int(query_id), cache_time=1, alert=True, message='اکانتی یافت نشد ❗️'))
            else:
                step = 'sendViewToPost'
                my_keyboard = [
                    [InlineKeyboardButton('🔙', callback_data='backToMenu')],
                ]
                await bot.edit_message_text(chat_id, message_id, '<b>- لطفا لینک پست مورد نظر را ارسال نمایید :</b>', reply_markup=InlineKeyboardMarkup(my_keyboard))

        elif data == 'reportPostPublic':
            step = 'reportPostPublic'
            my_keyboard = [
                    [InlineKeyboardButton('🔙', callback_data='backToMenu')],
                ]
            await bot.edit_message_text(chat_id, message_id, '<b>لطفا لینک پست کانال|گروه مورد نظر را ارسال نمایید :</b>', reply_markup=InlineKeyboardMarkup(my_keyboard))

        elif data == 'reActionEval':
            step = 'reActionEval'
            my_keyboard = [
                    [InlineKeyboardButton('🔙', callback_data='backToMenu')],
                ]
            await bot.edit_message_text(chat_id, message_id, '<b>لطفا در خط اول لینک پست موردنظر و در خط دوم ایموجی ها با فاصله و در خط سوم تعداد موردنظرتان را وارد نمایید :</b>', reply_markup=InlineKeyboardMarkup(my_keyboard))
        
        elif data == 'voteEval':
            step = 'voteEval'
            my_keyboard = [
                    [InlineKeyboardButton('🔙', callback_data='backToMenu')],
                ]
            await bot.edit_message_text(chat_id, message_id, '<b>لطفا در خط اول لینک پست و در خط دوم شماره گزینه موردنظرتان را وارد کنید (گزینه ها از 0 شروع میشوند) :</b>', reply_markup=InlineKeyboardMarkup(my_keyboard))

        elif data == 'blockEval':
            step = 'blockEval'
            my_keyboard = [
                    [InlineKeyboardButton('🔙', callback_data='backToMenu')],
                ]
            await bot.edit_message_text(chat_id, message_id, '<b>یوزرنیم کاربر مورد نظرتان را با @ وارد کنید :</b>', reply_markup=InlineKeyboardMarkup(my_keyboard))


#           Text Response            #
@bot.on_message(filters.text & filters.private & filters.user(bot_admins))
async def TextResponse(client, message):
    global step, isWorking, tempClient, api_hash, api_id, sleeping
    chat_id = message.chat.id
    text = message.text
    my_keyboard = [
        [InlineKeyboardButton('🔙', callback_data='backToMenu')],
    ]

#                       Add Account                       #if step == 'getPhoneForLogin' and text.replace('+', '').replace(' ', '').replace('-', '').isdigit():
    phone_number = text.replace('+', '').replace(' ', '').replace('-', '')
    if os.path.isfile(f'sessions/{phone_number}.session'):
        await message.reply('<b>این شماره از قبل در پوشه sessions سرور موجود است !</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
    else:
        tempClient['number'] = phone_number
        # ایجاد کلاینت با test_mode=True فقط برای ارسال کد
        tempClient['client'] = Client(f'sessions/{phone_number}', int(api_id), api_hash, test_mode=True)
        await tempClient['client'].connect()
        try:
            tempClient['response'] = await tempClient['client'].send_code(phone_number)
        except (errors.BadRequest, errors.PhoneNumberBanned, errors.PhoneNumberFlood, errors.PhoneNumberInvalid):
            await message.reply('<b>خطایی رخ داد !</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
        else:
            step = 'get5DigitsCode'
            await message.reply(f'<b>کد 5 رقمی به شماره {phone_number} ارسال شد ✅</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)

    elif step == 'get5DigitsCode' and text.replace(' ', '').isdigit():
        telegram_code = text.replace(' ', '')
    try:
        await tempClient['client'].sign_in(tempClient['number'], tempClient['response'].phone_code_hash, telegram_code)
        await tempClient['client'].disconnect()
        tempClient = {}
        step = 'getPhoneForLogin'
        await message.reply('<b>اکانت با موفقیت ثبت شد ✅\nدرصورتیکه قصد افزودن شماره دارید, شماره موردنظر را ارسال کنید و یا از دستور /cancel استفاده نمایید.</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
    except errors.PhoneCodeExpired:
        await tempClient['client'].disconnect()
        tempClient = {}
        step = None
        await message.reply('<b>کد ارسال شده منقضی شده است, لطفا عملیات را /cancel کنید و مجدد تلاش کنید.</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
    except errors.PhoneCodeInvalid:
        await message.reply('<b>کد وارد شده اشتباه است یا منقضی شده, لطفا از دستور /cancel استفاده نمایید و یا کد درست را ارسال کنید.</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
    except errors.BadRequest:
        await message.reply('<b>کد وارد شده اشتباه است یا منقضی شده, لطفا از دستور /cancel استفاده نمایید و یا کد درست را ارسال کنید.</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
    except errors.AuthKeyUnregistered:
        await asyncio.sleep(3)
        name = await randomString()
        try:
            await tempClient['client'].sign_up(tempClient['number'], tempClient['response'].phone_code_hash, name)
        except Exception:
            pass
        await tempClient['client'].disconnect()
        tempClient = {}
        step = 'getPhoneForLogin'
        await message.reply('<b>اکانت با موفقیت ثبت شد ✅\nدرصورتیکه قصد افزودن شماره دارید, شماره موردنظر را ارسال کنید و یا از دستور /cancel استفاده نمایید.</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
    except errors.SessionPasswordNeeded:
        step = 'SessionPasswordNeeded'
        await message.reply('<b>لطفا رمز تایید دو مرحله ای را وارد نمایید :</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)

    elif step == 'SessionPasswordNeeded':
        twoFaPass = text
        try :
            await tempClient['client'].check_password(twoFaPass)
        except errors.BadRequest:
            await message.reply('<b>رمز وارد شده اشتباه میباشد, لطفا مجدد ارسال نمایید یا از دستور /cancel استفاده نمایید.</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
        else:
            await tempClient['client'].disconnect()
            tempClient = {}
            step = 'getPhoneForLogin'
            await message.reply('<b>اکانت با موفقیت ثبت شد ✅\nدرصورتیکه قصد افزودن شماره دارید, شماره موردنظر را ارسال کنید و یا از دستور /cancel استفاده نمایید.</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)

#                       Delete Account                       #
    if step == 'removeAccount':
        step = None
        phone_number = text.replace('+', '').replace(' ', '').replace('-', '')
        if not os.path.isfile(f'sessions/{phone_number}.session'):
            await message.reply('<b>شماره مورد نظر در سرور یافت نشد !</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
        else:
            await bot.send_document(message.chat.id, f'sessions/{phone_number}.session', caption='<b>شماره مورد نظر با موفقیت حذف شد ✅\nسشن پایروگرام برای بایگانی برای شما ارسال شد.</b>', reply_markup=InlineKeyboardMarkup(my_keyboard))
            os.unlink(f'sessions/{phone_number}.session')

#                       set Time                       #
    if step == 'setTime':
        step = None
        sleeping = float(text)
        await message.reply('<b>زمان جدید با موفقیت تنظیم شد ✅</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)

#                       join Accounts                       #
    if step == 'joinAccounts':
        step = None
        evalID = await randomString()
        isWorking.append(evalID)
        link = text.split()[0].replace('@', '').replace('+', 'joinchat/')
        allAcccounts = len((await accountList()))
        all = 0
        error = 0
        done = 0
        TS = time.time()
        msg = await message.reply('<b>عملیات عضویت شروع شد ...</b>')
        for session in ((await accountList())):
            if evalID not in isWorking:
                break
            all += 1
            await asyncio.sleep(sleeping)
            try:
                api_id2, api_hash2 = await randomAPP()
                cli = Client(f'sessions/{session}', api_id2, api_hash2)
                await cli.connect()
                await asyncio.sleep(0.2)
                await cli.join_chat(link)
                await asyncio.sleep(0.2)
                await cli.disconnect()
            except Exception as e:
                try:
                    await cli.disconnect()
                except:
                    pass
                error += 1
            else:
                done += 1
            finally:
                spendTime = await remainTime(TS)
                await bot.edit_message_text(chat_id, msg.id, f'''♻️ عملیات عضویت اکانت های ربات ...

• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}

برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
        try:
            isWorking.remove(evalID)
        except:
            pass
        spendTime = await remainTime(TS)
        await message.reply(f'''<b>عملیات عضویت با موفقیت به پایان رسید ✅

• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}</b>''', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)


#                       Leave Accounts                       #
    if step == 'leaveAccounts':
        step = None
        evalID = await randomString()
        isWorking.append(evalID)
        allAcccounts = len((await accountList()))
        all = 0
        error = 0
        done = 0
        TS = time.time()
        msg = await message.reply('<b>عملیات خروج شروع شد ...</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
        for session in ((await accountList())):
            if evalID not in isWorking:
                break
            all += 1
            await asyncio.sleep(sleeping)
            try:
                api_id2, api_hash2 = await randomAPP()
                cli = Client(f'sessions/{session}', api_id2, api_hash2)
                await cli.connect()
                await asyncio.sleep(0.2)
                await cli.leave_chat(int(text), delete=True)
                await asyncio.sleep(0.2)
                await cli.disconnect()
            except Exception as e:
                try:
                    await cli.disconnect()
                except:
                    pass
                error += 1
            else:
                done += 1
            finally:
                spendTime = await remainTime(TS)
                await bot.edit_message_text(chat_id, msg.id, f'''♻️ عملیات لفت اکانت های ربات ...

• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}

برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
        try:
            isWorking.remove(evalID)
        except:
            pass
        spendTime = await remainTime(TS)
        await message.reply(f'''<b>عملیات لفت با موفقیت به پایان رسید ✅</b>

• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)

#                       send view                       #
    if step == 'sendViewToPost':
        step = None
        evalID = await randomString()
        isWorking.append(evalID)
        username = text.split('/')[3]
        msg_id = int(text.split('/')[4])
        allAcccounts = len((await accountList()))
        all = 0
        error = 0
        done = 0
        TS = time.time()
        msg = await message.reply('<b>عملیات ویو پست کانال شروع شد ...</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
        for session in ((await accountList())):
            if evalID not in isWorking :
                break
            try:
                await cli.disconnect()
            except:
                pass
            all += 1
            await asyncio.sleep(sleeping)
            try:
                api_id2, api_hash2 = await randomAPP()
                cli = Client(f'sessions/{session}', api_id2, api_hash2)
                await cli.connect()
                await asyncio.sleep(0.2)
                await cli.invoke(functions.messages.GetMessagesViews(peer = await cli.resolve_peer(username), id=[msg_id], increment=True))
                await asyncio.sleep(0.2)
                await cli.disconnect()
            except Exception as e:
                try:
                    await cli.disconnect()
                except:
                    pass
                error += 1
            else:
                done += 1
            finally:
                spendTime = await remainTime(TS)
                await bot.edit_message_text(chat_id, msg.id, f'''♻️ عملیات ارسال ویو اکانت های ربات ...

• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}

برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
        try:
            isWorking.remove(evalID)
        except:
            pass
        spendTime = await remainTime(TS)
        await message.reply(f'''<b>عملیات بازدید پست کانال با موفقیت به پایان رسید ✅</b>

• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)


#                       send Public Post Roport                       #
    if step == 'reportPostPublic':
        step = None
        evalID = await randomString()
        isWorking.append(evalID)
        if text.split('/')[3] != 'c':
            peerID = '@' + text.split('/')[3]
            peerMessageID = int(text.split('/')[4])
        else:
            peerID = int('-100' + text.split('/')[4])
            peerMessageID = int(text.split('/')[5])
        allAcccounts = len((await accountList()))
        all = 0
        error = 0
        done = 0
        TS = time.time()
        if text.split('/')[3].isdigit():
            await message.reply('<b>لینکی که برام ارسال کردی مربوط به یک چت خصوصیه ❗️</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
        else:
            msg = await message.reply('<b>عملیات ریپورت پست عمومی شروع شد ...</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
            for session in ((await accountList())):
                if evalID not in isWorking:
                    break
                try:
                    await cli.disconnect()
                except:
                    pass
                all += 1
                await asyncio.sleep(sleeping)
                try:
                    api_id2, api_hash2 = await randomAPP()
                    cli = Client(f'sessions/{session}', api_id2, api_hash2)
                    await cli.connect()
                    await asyncio.sleep(0.2)
                    await cli.invoke(functions.messages.Report(peer= await cli.resolve_peer(peerID), id=[peerMessageID], reason=types.InputReportReasonPornography(), message=''))
                    await asyncio.sleep(0.2)
                    await cli.disconnect()
                except Exception as e:
                    try:
                        await cli.disconnect()
                    except:
                        pass
                    error += 1
                else:
                    done += 1
                finally:
                    spendTime = await remainTime(TS)
                    await bot.edit_message_text(chat_id, msg.id, f'''♻️ عملیات ریپورت پست کانال ...

• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}

برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
            try:
                isWorking.remove(evalID)
            except:
                pass
            spendTime = await remainTime(TS)
            await message.reply(f'''<b>عملیات ریپورت پست با موفقیت به پایان رسید ✅</b>

• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)

#                       send Post reAction                       #
    if step == 'reActionEval':
        step = None
        evalID = await randomString()
        isWorking.append(evalID)
        peerID = '@' + text.split("\n")[0].split('/')[3]
        peerMessageID = int(text.split("\n")[0].split('/')[4])
        emojies = text.split("\n")[1].split()
        countOfWork = int(text.split("\n")[2])
        allAcccounts = len((await accountList()))
        all = 0
        error = 0
        done = 0
        TS = time.time()
        if text.split("\n")[0].split('/')[3].isdigit():
            await message.reply('<b>لینکی که برام ارسال کردی مربوط به یک چت خصوصیه ❗️</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
        else:
            msg = await message.reply('<b>عملیات ارسال ری اکشن شروع شد ...</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
            for session in ((await accountList())):
                if all >= countOfWork:
                    break
                if evalID not in isWorking:
                    break
                try:
                    await cli.disconnect()
                except:
                    pass
                all += 1
                await asyncio.sleep(sleeping)
                try:
                    api_id2, api_hash2 = await randomAPP()
                    cli = Client(f'sessions/{session}', api_id2, api_hash2)
                    await cli.connect()
                    await asyncio.sleep(0.2)
                    await cli.send_reaction(peerID, peerMessageID, random.choice(emojies))
                    await asyncio.sleep(0.2)
                    await cli.disconnect()
                except Exception as e:
                    try:
                        await cli.disconnect()
                    except:
                        pass
                    error += 1
                else:
                    done += 1
                finally:
                    spendTime = await remainTime(TS)
                    await bot.edit_message_text(chat_id, msg.id, f'''♻️ عملیات ارسال ری اکشن پست کانال ...

• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}

برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
            try:
                isWorking.remove(evalID)
            except:
                pass
            spendTime = await remainTime(TS)
            await message.reply(f'''<b>عملیات ری اکشن پست با موفقیت به پایان رسید ✅</b>

• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)

#                       send Post vote                       #
    if step == 'voteEval':
        step = None
        evalID = await randomString()
        isWorking.append(evalID)
        peerID = '@' + text.split("\n")[0].split('/')[3]
        peerMessageID = int(text.split("\n")[0].split('/')[4])
        opt = text.split("\n")[1]
        allAcccounts = len((await accountList()))
        all = 0
        error = 0
        done = 0
        TS = time.time()
        if not opt.isdigit():
            await message.reply('<b>گزینه وارد شده صحیح نمیباشد ❗️</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
        else:
            msg = await message.reply('<b>عملیات ارسال نظر سنجی شروع شد ...</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
            for session in ((await accountList())):
                if evalID not in isWorking:
                    break
                try:
                    await cli.disconnect()
                except:
                    pass
                all += 1
                await asyncio.sleep(sleeping)
                try:
                    api_id2, api_hash2 = await randomAPP()
                    cli = Client(f'sessions/{session}', api_id2, api_hash2)
                    await cli.connect()
                    await asyncio.sleep(0.2)
                    await cli.vote_poll(peerID, peerMessageID, int(opt))
                    await asyncio.sleep(0.2)
                    await cli.disconnect()
                except Exception as e:
                    try:
                        await cli.disconnect()
                    except:
                        pass
                    error += 1
                else:
                    done += 1
                finally:
                    spendTime = await remainTime(TS)
                    await bot.edit_message_text(chat_id, msg.id, f'''♻️ عملیات ارسال نظرسنجی ...

• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}

برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
            try:
                isWorking.remove(evalID)
            except:
                pass
            spendTime = await remainTime(TS)
            await message.reply(f'''<b>عملیات نظر سنجی با موفقیت به پایان رسید ✅</b>

• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)


#                       block users                       #
    if step == 'blockEval':
        step = None
        evalID = await randomString()
        isWorking.append(evalID)
        peerID = text.replace('@', '')
        allAcccounts = len((await accountList()))
        all = 0
        error = 0
        done = 0
        TS = time.time()
        msg = await message.reply('<b>عملیات ارسال نظر سنجی شروع شد ...</b>', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)
        for session in ((await accountList())):
            if evalID not in isWorking:
                break
            try:
                await cli.disconnect()
            except:
                pass
            all += 1
            await asyncio.sleep(sleeping)
            try:
                api_id2, api_hash2 = await randomAPP()
                cli = Client(f'sessions/{session}', api_id2, api_hash2)
                await cli.connect()
                await asyncio.sleep(0.2)
                await cli.block_user(peerID)
                await asyncio.sleep(0.2)
                await cli.disconnect()
            except Exception as e:
                try:
                    await cli.disconnect()
                except:
                    pass
                error += 1
            else:
                done += 1
            finally:
                spendTime = await remainTime(TS)
                await bot.edit_message_text(chat_id, msg.id, f'''♻️ عملیات بلاک کاربر ...

• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}

برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
        try:
            isWorking.remove(evalID)
        except:
            pass
        spendTime = await remainTime(TS)
        await message.reply(f'''<b>عملیات بلاک کاربر با موفقیت به پایان رسید ✅</b>

• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''', reply_markup=InlineKeyboardMarkup(my_keyboard), quote=True)











bot.run()
