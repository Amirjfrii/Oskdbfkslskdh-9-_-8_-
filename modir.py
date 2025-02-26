from telethon.sync import TelegramClient,functions, events, errors
from telethon.tl.custom import Button
from telethon.sessions import StringSession
import sqlite3, os, random, json
from telethon.tl.functions.channels import InviteToChannelRequest

# ======================= APIs =============================
api_id = 000000000
api_hash = "00000000000"

owner = 0000000000

# ======================= client ===========================
bot = TelegramClient('younes', api_id, api_hash)
bot.start(bot_token="00000000")
# =========================== markups ======================
main_markup =  [
        [Button.text('📤 ارسال اکانت', resize=True)],
        [Button.text('☎️ پشتیبانی', resize=True), Button.text('👤 حساب کاربری', resize=True)],
        [Button.text('✅ تسویه حساب', resize=True)],
    ]
admin_markup =  [
        [Button.text('🔆 ثبت سفارش 🔆', resize=True)],
        [Button.text('🌐 افزودن پروکسی 🌐', resize=True), Button.text('👤 امار ربات 👤', resize=True)],
        [Button.text('🔙 بازگشت', resize=True)],
    ] 
cancel_markup =  [
        [Button.text('🔙 بازگشت', resize=True)],
    ]
admin_ancel_markup =  [
        [Button.text('🔙 برگشت', resize=True)],
    ]
# ======================= db settings ======================
conn = sqlite3.connect("data.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS `users` (`user_id` BIGINT(10), `step` VARCHAR(1000), `balance` INT(5) DEFAULT 0, `is_admin` BOOLEAN DEFAULT(0));")
cursor.execute("CREATE TABLE IF NOT EXISTS `sessions` (`number` VARCHAR(100), `proxy` VARCHAR(255), `password` text(10), `verifaid` BOOLEAN DEFAULT(0));")
cursor.execute("CREATE TABLE IF NOT EXISTS `orders` (`hash` VARCHAR(10), `needen_count` INT(10), `sent_count` INT(10), `dest_id` VARCHAR(255));")
cursor.execute("CREATE TABLE IF NOT EXISTS `proxies` (`proxy` VARCHAR(1000), `used_count` INT(3));")
conn.commit()
# ==================== helper funcs ========================
def query(query):
    result = cursor.execute(query)
    conn.commit()
    return result

def insert_user(user):
    cursor.execute(f"INSERT INTO `users` (`user_id`, `step`) VALUES ('{user}', 'none');")

def set_step(user, step):
    query(f"UPDATE `users` SET `step` = '{step}' WHERE `user_id` = '{user}'")

def make_hash():
    chars = list("qwertyuioplkjhgfdsazxcvbnm")
    random.shuffle(chars)
    order_hash = "".join(chars[0:10])
    return order_hash

def get_proxy():
    proxies = cursor.execute("SELECT * FROM `proxies`").fetchall()
    if not len(proxies):
        return False
    proxies.sort(key=lambda x : x[1])
    proxy = proxies[0]
    return proxy

def delete_acc(phone):
    query(f"DELETE FROM `sessions` WHERE `number` = '{phone}' LIMIT 1")
    os.remove(f"sessions/{phone}.session")

def make_hash():
    letters = list("1234567890qwertyuioplkjhgfdsazxcvbnm")
    random.shuffle(letters)
    return "".join(letters[0:5])

async def is_signed_up(jtext):
    try:
        s = json.loads(jtext.to_json())
        if s['_'] == 'AuthorizationSignUpRequired':
            return False
        else:
            return True
    except Exception:
        return True
# ====================== main function =====================
@bot.on(events.NewMessage)
async def answer(event):
    message = event.message
    text = event.raw_text
    chat_id = event.sender_id
    
    if chat_id == owner:
        main_markup.append([Button.text('💫 پنل مدیریت', resize=True)])
    # ======================================================
    insert_user(chat_id)
    step = cursor.execute(f"SELECT `step` FROM `users` WHERE `user_id` = '{chat_id}'").fetchone()[0]
    if text.lower() == '/start':
        await event.reply('👋 سلام خوش اومدی .  \n\n👈 برای ادامه از منوی زیر انتخاب کن :', buttons=main_markup)
        set_step(chat_id, "none")
    elif text == "🔙 بازگشت":
        await event.reply('🏠 برگشتیم به منوی اصلی !\n\n👈 برای ادامه از منوی زیر انتخاب کن :', buttons=main_markup)
        set_step(chat_id, "none")
    # ==================================================
    elif text == "💫 پنل مدیریت":
        set_step(chat_id, "none")
        await event.reply(f"✅ به پنل مدیریت خوش آمدید !", buttons=admin_markup)
    elif text == "🔙 برگشت":
        set_step(chat_id, "none")
        await event.reply(f"✅ برگشتیم به منوی اصلی !", buttons=admin_markup)
    # ==================================================
    elif text == "👤 امار ربات 👤":
        count = len( cursor.execute("SELECT * FROM `sessions` WHERE `verifaid` = '1'").fetchall() )
        await event.reply(f'👤 ربات شما دارای {count} اکانت سالم می باشد ... !', buttons=admin_markup)
        set_step(chat_id, "none")
    # ==================================================
    elif text == "📤 ارسال اکانت":
        await event.reply('📞 لطفا شماره ی اکانت را ارسال نمایید :\n\n👈 نمونه : +989120000000', buttons=cancel_markup)
        set_step(chat_id, "send_account")
    elif step == "send_account":
        if text.startswith("+"):
            await event.reply('♻️ در حال پردازش...\n🙏 لطفا منتظر بمانید .', buttons=cancel_markup)
            phone = text.replace(" ", "")

            proxy = get_proxy()
            if not proxy:
                await event.reply('‼️ لطفا ابتدا یک پروکسی به ربات اضافه نموده و سپس اکانت ارسال کنید ... !', buttons=main_markup)
                set_step(chat_id, "none")
                return


            proxy = proxy[0]
            IP, port, username, password = proxy.split(":")
            print(IP, port, username, password)
            account = TelegramClient(f"sessions/{phone}", api_id , api_hash, proxy=("socks5", IP, int(port), True, username, password))

            await account.connect()
            if await account.is_user_authorized():
                await bot.send_message(chat_id, f'❌ شماره در حال حاضر بر روی ربات موجود است ... !\n🙏 لطفا شماره ی دیگری را ارسال کنید :')
                return
            try:
                auth = await account.send_code_request(phone, force_sms=False, test_mode=True)
                set_step(chat_id, f'auth1:{phone}:{auth.phone_code_hash}')
                await bot.send_message(chat_id, f'🔢 کد دریافتی بر روی شماره {phone} را ارسال نمایید.')
                query(f"INSERT INTO `sessions` (`number`, `proxy`, `password`, `verifaid`) VALUES ('{phone}', '{proxy}', NULL, '0');")
            except errors.PhoneNumberBannedError:
                await bot.send_message(chat_id, f'⚠️خطا در ارسال کد به شماره {phone}\nشماره شما از تلگرام مسدود شده است !\n🙏 لطفا شماره ی دیگری را ارسال کنید :')
                await account.disconnect()
                os.remove(f'sessions/{phone}.session')
            except errors.PhoneNumberInvalidError:
                await bot.send_message(chat_id, f'⚠️ شماره {phone} اشتباه است.')
                await account.disconnect()
                os.remove(f'sessions/{phone}.session')
            except errors.FloodWaitError as e3:
                await bot.send_message(chat_id, f'⏳ شماره {phone} از سمت تلگرام محدود شده است و تا {e3.seconds} ثانیه دیگر قابل ثبت نیست.')
                await account.disconnect()
                os.remove(f'sessions/{phone}.session')
            except errors.PhoneNumberOccupiedError:
                await bot.send_message(chat_id, '⚠️خطا در ارسال کد !')
                await account.disconnect()
                os.remove(f'sessions/{phone}.session')
            except errors.PhoneNumberUnoccupiedError:
                await bot.send_message(chat_id, '⚠️خطا در ارسال کد !')
                await account.disconnect()
                os.remove(f'sessions/{phone}.session')
            except ConnectionError:
                await bot.send_message(dev,f'پروکسی  {proxy} دچار مشکل شده است و نمیتوان با ان ارتباط بر قرار کرد.')
                await bot.send_message(chat_id, '❌ارور در ارسال کد لطفا دوباره امتحان کنید.')
                await account.disconnect()
                os.remove(f'sessions/{phone}.session')
            except Exception as error:
                await bot.send_message(2002159549, f'⚠️ مشکلی در ربات Contact adder پیش آمد !\nجزئیات : \n`{error}`')
                await bot.send_message(chat_id, '⚠️ خطایی ناشناخته در ارسال کد !')
                await account.disconnect()
                os.remove(f'sessions/{phone}.session')
        else:
            await event.reply(f"⚠️ شماره {text} درست ارسال نشده است ! با توجه به نمونه ارسال کنید :\n\n📞 +989120000000")
    elif step.startswith("auth1:"):
        if text.isdigit():
            msg = await event.reply('🙏لطفا کمی صبر کنید ...')
            try:
                nothing, phone, phone_code_hash= step.split(':')


                result = cursor.execute(f"SELECT * FROM `sessions` WHERE `number` = '{phone}' LIMIT 1")
                number, proxy, password, verifaid = result.fetchone()

                IP, port, username, password = proxy.split(":")
                print(IP, port, username, password)


                account = TelegramClient("sessions/"+phone, api_id , api_hash , proxy=("socks5" , IP , int(port), True,  username, password))
                await account.connect()

                result = await account(functions.auth.SignInRequest(phone_number=phone, phone_code_hash=phone_code_hash,phone_code=text))
                isSignedUp = await is_signed_up(result)
                if isSignedUp == True:
                    query(f"UPDATE `proxies` SET `used_count` = used_count + 1 WHERE `proxy` = '{proxy}'")
                    query(f"UPDATE `sessions` SET `verifaid` = '1' WHERE `number` = '{phone}' LIMIT 1")
                    set_step(chat_id, "none")
                    await bot.send_message(chat_id, f'🔐 اکانت `{phone}` دریافت شد!\n\n👈 در صورت تمایل شماره ی بعدی را ارسال یا بر روی دکمه ی کنسل کلیک کنید .', buttons=[
                        [Button.inline(f'دریافت موجودی', f'tayid|{time.time()}|False|{phone}')],
                    ])
                else:
                    await bot.send_message(chat_id, '⚠️ خطا اکانت وارد شده در تلگرام ثبت نشده است.\n🙏 لطفا ابتدا خودتان با تلگرام وارد اکانت شده و سپس اکانت را برای ربات ارسال کنید\n\n👈 در صورت تمایل شماره ی بعدی را ارسال یا بر روی دکمه ی کنسل کلیک کنید .', buttons=cancel_markup)
                    delete_acc(phone)
                account.disconnect()
            except errors.SessionPasswordNeededError:
                await bot.send_message(chat_id, f'🔑 تایید دو مرحله ای شماره {phone} را وارد کنید.', buttons=cancel_markup)
                set_step(chat_id, f'auth2:{phone}')
                account.disconnect()
            except errors.PhoneCodeExpiredError:
                await bot.send_message(chat_id, '⚠️ خطا - کد ارسال شده منقضی شده است لطفا دوباره مراحل را طی کنید !', buttons=main_markup)
                delete_acc(phone)
                set_step(chat_id, "none")
                account.disconnect()
            except errors.PhoneCodeInvalidError:
                await bot.send_message(chat_id, '❌ کد وارد شده اشتباه میباشد لطفا دوباره کد را ارسال کنید :', buttons=cancel_markup)
                account.disconnect()
            except ConnectionError:
                await bot.send_message(2002159549, f'❌ مشکلی در پروکسی {proxy} ایجاد شده است ... !\nپروکسی از ربات حذف شد !\nدر صورتی تمایل می توانید دوباره پروکسی را به ربات اضافه کنید !')
                await bot.send_message(2002159549, proxy)

                await bot.send_message(chat_id, '❌ مشکلی در ارتباط با سرور به وجود آمد !\n🙏 لطفا مراحل را از اول دوباره طی کنید .', buttons=main_markup)
                delete_acc(phone)

                set_step(chat_id, "none")
                account.disconnect()
            except Exception as error:
                await bot.send_message(2002159549, f'⚠️ مشکلی در ربات Contact adder پیش آمد !\nجزئیات : \n`{error}`')
                await bot.send_message(chat_id, '⚠️ خطای ناشناخته لطفا دوباره مراحل را طی کنید !', buttons=main_markup)
                delete_acc(phone)
                set_step(chat_id, 'none')
                account.disconnect()
        else:
            await event.reply('⚠️ کد ارسالی اشتباه است.\n👈 شما می توانید کد صحیح را ارسال یا کنسل کنید .', buttons=cancel_markup)
    elif step.startswith('auth2'):
        await event.reply('🙏 لطفا کمی صبر کنید ...')
        try:
            nothing, phone = step.split(':')


            result = cursor.execute(f"SELECT * FROM `sessions` WHERE `number` = '{phone}' LIMIT 1")
            number, proxy, password, verifaid = result.fetchone()

            IP, port, username, password = proxy.split(":")
            print(IP, port, username, password)


            account = TelegramClient("sessions/" + phone, api_id , api_hash , proxy=("socks5" , IP , int(port), True,  username, password))

            await account.connect()
            await account.sign_in(password=text)
            query(f"UPDATE `proxies` SET `used_count` = used_count + 1 WHERE `proxy` = '{proxy}'")
            query(f"UPDATE `sessions` SET `verifaid` = '1' WHERE `number` = '{phone}' LIMIT 1")

            await bot.send_message(chat_id, f'🔐 اکانت `{phone}` دریافت شد!\n\n👈 در صورت تمایل شماره ی بعدی را ارسال یا بر روی دکمه ی کنسل کلیک کنید .', buttons=[
                [Button.inline(f'دریافت موجودی', f'tayid|{time.time()}|{text}|{phone}')],
            ])
        except errors.PasswordHashInvalidError:
            await bot.send_message(chat_id, '⚠️ تایید دو مرحله ای  اشتباه است.\n👈 دوباره ارسال کنید یا کنسل کنید :', buttons=cancel_markup)
        except ConnectionError:
            await bot.send_message(2002159549, f'❌ مشکلی در پروکسی {proxy} ایجاد شده است ... !\nپروکسی از ربات حذف شد !\nدر صورتی تمایل می توانید دوباره پروکسی را به ربات اضافه کنید !')
            await bot.send_message(2002159549, proxy)

            await bot.send_message(chat_id, '❌ مشکلی در ارتباط با سرور به وجود آمد !\n🙏 لطفا مراحل را از اول دوباره طی کنید .', buttons=cancel_markup)
            delete_acc(phone)
            set_step(chat_id,'none')
        except Exception as e:
            await bot.send_message(2002159549, f'⚠️ مشکلی در ربات Contact adder پیش آمد !\nجزئیات : \n`{error}`')

            await bot.send_message(chat_id, '⚠️ خطای ناشناخته لطفا دوباره مراحل را طی کنید !', buttons=main_markup)
            delete_acc(phone)
            set_step(chat_id, "none")
        finally:
            await account.disconnect()
    # ======================================================
    elif text == "☎️ پشتیبانی" :
        await event.reply("👮🏻 همکاران ما در خدمت شما هستن\n\n* سعی بخش پشتیبانی بر این است که تمامی پیام های دریافتی در کمتر از ۱۲ ساعت پاسخ داده شوند، بنابراین تا زمان دریافت پاسخ صبور باشید\n\nلطفا پیام، سوال، پیشنهاد و یا انتقاد خود را در قالب یک پیام واحد به طور کامل ارسال کنید 👇🏻",  buttons=cancel_markup)
        set_step(chat_id, "support")
    elif step == "support":
        await event.reply(f"✅ با موفقیت پیام به پشتیبانی ارسال شد !", buttons=main_markup)
        await bot.send_message(owner, f'پیام از طرف `{chat_id}`:\n\n{text}\n\n\nجهت ارسال پاسخ ابتدا بر روی /send_{chat_id} ککلیک کنید !')
        set_step(chat_id, 'none')
    elif text.startswith("/send") and chat_id == owner:
        set_step(chat_id, text)
        await event.reply("✅ متن پیام را ارسال کنید :", buttons=cancel_markup)
    elif step.startswith("/send"):
        set_step(chat_id, 'none')
        ui = step.replace("/send_", "")
        await event.reply(f"✅ پیام با موفقیت به {ui} ارسال شد !", buttons=main_markup)
        await bot.send_message(int(ui), f'یک پاسخ از طرف مدیریت دارید ! :\n\n{text}')
    elif text == "👤 حساب کاربری":
        balance = query(f"SELECT `balance` FROM `users` WHERE `user_id` = '{chat_id}'").fetchone()[0]
        await event.reply(f"🆔 شناسه : {chat_id}\n📤 موجودی حساب : {balance} اکانت")
    elif text == "🌐 افزودن پروکسی 🌐":
        await event.reply(f"👈 لطفا فایل پروکسی ها را با فرمت زیر ارسال کنید :\n\nIP:PORT:USERNAME:PASSWORD\n1.1.1.1:443:username:pass", buttons=admin_ancel_markup)
        set_step(chat_id, "add_proxy")
    elif step == "add_proxy":
        file_name = message.file.name
        await bot.download_media(message)

        with open(file_name, "r") as f:
            proxies = f.read().split("\n")
            for proxy in proxies:
                try:
                    if len(proxy.split(":")) == 4:
                        query(f"INSERT INTO `proxies` (`proxy`, `used_count`) VALUES ('{proxy}', '0')")
                except:
                    pass
        os.remove(file_name)

        await event.reply(f"✅ با موفقیت اضافه شد ...!\n\n👈 در صورت تمایل پروکسی های بعدی را ارسال یا برو روی دکمه ی کنسل کلیک کنید ... !")
# ==========================================================
@bot.on(events.CallbackQuery)
async def callback(events):
    callback = events.data.decode()
    if callback.startswith('tayid'):
        if time.time() - int(callback.split('|')[1].split('.')[0]) >= int(600):
            await events.answer('کمی صبر کنید ...')
            phone = callback.split("|")[-1]
            
            
            
            result = cursor.execute(f"SELECT * FROM `sessions` WHERE `number` = '{phone}' LIMIT 1")
            number, proxy, password, verifaid = result.fetchone()

            IP, port, username, password = proxy.split(":")
            client = TelegramClient("Accounts/"+callback.split('|')[-1], api_id , api_hash , proxy=("socks5" , IP , int(port), True,  username, password))
            await client.connect()
            
            s = callback.split("|")
            try:
                result = await client(functions.account.GetAuthorizationsRequest())
                if len(result.authorizations) == 1:
                    if s[-2] != 'False':
                        await client.edit_2fa(current_password=s[-2],new_password="@number1729")
                        if phone.startswith("+62"):
                            coin = 12000
                        elif phone.startswith("+1") and len(phone) == 12:
                            coin = 10000
                        else:
                            coin = 5000
                        query(f"UPDATE `users` SET `balance` = balance + {coin} WHERE `user_id` = '{chat_id}'")
                        await events.edit(f'🎉 تبریک، شماره {phone} تایید شد و {coin} سکه به حسابتان اضافه شد!')                        
                    else:
                        await client.edit_2fa(new_password="@wo4ka")
                        if phone.startswith("+62"):
                            coin = 12000
                        elif phone.startswith("+1") and len(phone) == 12:
                            coin = 10000
                        else:
                            coin = 5000
                        query(f"UPDATE `users` SET `balance` = balance + {coin} WHERE `user_id` = '{chat_id}'")
                        await events.edit(f'🎉 تبریک، شماره {phone} تایید شد و {coin} سکه به حسابتان اضافه شد!')                        
                    shutil.move(f"Accounts/{phone}.session", f"Success/{phone}.session".format(phone))# move it
                    os.system(f"screen -dm bash -c 'python3 Plugins/delete.py {phone}'")
                else:
                    await events.reply('⚠️ نشستهای فعال اکانت خالی نیست.')
            except errors.UserDeactivatedBanError:
                await events.edit('⚠️متاسفانه اکانت شما دیلیت شده است لطفا اکانت دیگری را وارد نمایید.')

                os.remove("Accounts/{}.session".format(phone))   
            except errors.UserDeactivatedError:
                await events.edit('⚠️متاسفانه اکانت شما دیلیت شده است لطفا اکانت دیگری را وارد نمایید.')
         
                os.remove("Accounts/{}.session".format(phone))  
            except errors.SessionExpiredError:
                await events.edit(f'⚠️ شماره {phone} از دسترس ربات خارج شده است و امکان ثبت آن نیست.')
       
                os.remove("Accounts/{}.session".format(phone))    
            except errors.SessionRevokedError:
                await events.edit(f'⚠️ شماره {phone} از دسترس ربات خارج شده است و امکان ثبت آن نیست.')
              
                os.remove("Accounts/{}.session".format(phone))   
            except errors.rpcerrorlist.PasswordHashInvalidError:
                await events.edit(f'⚠️ تایید دو مرحله ای شماره {phone} تغییر کرده است و امکان ثبت آن نیست.')     
            
                os.remove("Accounts/{}.session".format(phone))   
            except Exception as e:
                await bot.send_message(349802221,f'Error ->\n{e}')
                await events.edit('⚠️خطای ناشناخته از تلگرام لطفا دوباره اکانت را وارد نمایید یا اکانت دیگری را وارد ربات نمایید.')
               
                os.remove("Accounts/{}.session".format(phone))   
            finally:
                await client.disconnect()
        else:
            await events.answer('هنوز 10 دقیقه نشده است لطفا {} ثانیه دیگر صبر کنید با تشکر'.format(str( 600 - (time.time() - int(callback.split('|')[[1]].split('.')[0]))  ).split('.')[0]))
        
# ==========================================================
bot.run_until_disconnected()
