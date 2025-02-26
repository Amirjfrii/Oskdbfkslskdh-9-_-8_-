from pyrogram import Client, filters
from pyrogram.types import *
from pyrogram.raw import functions , base , types
import json
import requests 
import os
import pathlib
import fnmatch





file=open("downloaded.txt","w")
file.write("0")
file.close()
try:
    os.mkdir("users")
except:
    pass


#=================================
#ساخته شده توسط @sourcemr
#کپی برداری بدون ذکر منبع حرام میباشد
#اگه دوست داری سر پل صراط جلوتو نگیرم منبع رو پاک نکن
#=================================

#متغير ها

api_id = 2802662 # ایپی ایدی
api_hash = 'b8a41227faa9481313ecfa661ef50ef4' # ایپی هش
bot_token = '7875185949:AAETxQvzQH2q2wTVjbRdT_ujCv35xWjV_FY' #توکن ربات
channel = "@infojafarbot" #یورزنیم چنل با @
botuser = "instagram_jafar_bot" #یوزرنیم ربات بدون @
addurl = f"http://telegram.me/{botuser}?startgroup=new" #دست نزنید
support = "@pv_mooz" #ایدی پشتیبانی با @
gp = f"/start@{botuser}" #دستور استارت در گروه
gph = f"/help@{botuser}" #دستور راهنما در گروه
admin = 1495973057 #ايدي عددي ادمين
bot1 = "on" #خاموش و روشني ربات
offtxt = "کاربر گرامي ربات فعلا آفلاین ميباشد" #متن خاموشي ربات
coin = 1 #سکه مورد نياز براي دانلود
coinprice = 100 #قيمت سکه به تومان
step = "none" #دست نزنيد
banned = [] #کاربران مسدود شده
coinuser = 0 #دست نزنيد
downloads = 0 #دست نزنيد






app = Client("sourcemr", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

help = InlineKeyboardMarkup(
     [
         [
             InlineKeyboardButton('📷راهنمای دانلودر',callback_data='dhelp'),
             InlineKeyboardButton('💬پشتیبانی',callback_data='supp') 

         ],
         [
             InlineKeyboardButton('❌️بستن راهنما',callback_data='close')
         ],
     ]
)



add = InlineKeyboardMarkup(
     [
         [
             InlineKeyboardButton("➕️افزودن ربات به گروه", url=addurl)
         ],
         [
             InlineKeyboardButton('🔙برگشت به من اصلی',callback_data='back')
         ],
     ]
)


gpbtn = InlineKeyboardMarkup(
     [
         [
             InlineKeyboardButton('🔙برگشت به من اصلی',callback_data='back')
         ],
     ]
)


adminbtn = [
    [KeyboardButton("آمار ربات")],[KeyboardButton("تنظيمات سکه")],
    [KeyboardButton("ربات خاموش")],[KeyboardButton("ربات روشن")],
    [KeyboardButton("مسدود کردن فرد")],[KeyboardButton("رفع مسدود کردن فرد")],
    [KeyboardButton("تنظيمات ربات")],
    [KeyboardButton("/start")],
]

coinbtn = [
    [KeyboardButton("افزودن سکه به کاربر")],[KeyboardButton("کسر سکه از کاربر")],
    [KeyboardButton("تنطيم سکه مورد نياز پست")],
    [KeyboardButton("رايگان کردن ربات")],[KeyboardButton("تعيين قيمت سکه")],
    [KeyboardButton("برگشت به منو اصلي")],
]





botbtn = [
    [KeyboardButton("تنظيم متن خاموشي")],
    [KeyboardButton("تغيير چنل جوين اجباري")],
    [KeyboardButton("برگشت به منو اصلي")],
]

backbtn = [
    [KeyboardButton("برگشت به منو اصلي")],
]

startbtn = [
    [KeyboardButton("راهنما")],
    [KeyboardButton("سازنده")],
    [KeyboardButton("----------------------------------------")],
    [KeyboardButton("سکه هاي من")],[KeyboardButton("خريد سکه")],
    [KeyboardButton("حساب کاربري و آمار")],
]

keyboard_m = ReplyKeyboardMarkup(adminbtn)
coin_m = ReplyKeyboardMarkup(coinbtn)
bot_m = ReplyKeyboardMarkup(botbtn)
start_m = ReplyKeyboardMarkup(startbtn)
back_m = ReplyKeyboardMarkup(backbtn)

starthelp = "به راهنمای ربات خوش امدید لطفا یک گزینه را انتخاب کنید"

supporttxt = f"جهت پشتیبانی به پیوی مراجعه کنید {support}"

helptxt = """
شما میتوانید از ربات در گروه و پیوی هم استفاده کنید
جهت استفاده در پیوی کافیست لینک پست یا استوری یا هرچیزی را بفرستید 
و سپس ربات شروع به دانلود کردن خواهد کرد

برای گروه هم کافیست اول عبارت insta را وارد کنید و سپس در کنار آن لینک پست یا استوری

استفاده از ربات هیچگونه محدودیتی ندارد
فقط یادتون باشه در چنل عضو باشید که ربات از کار نیفته

اگه هم خواستی میتونی با زدن دکمه زیر منو به گروهت بیاری

فقط یادت نره ادمینم کنی چون نمیتونم لینکارو دریافت کنم
    """

gptxt = "من در گروه اکنون ميتوانم فعاليت کنم براي دانلود اول عبارت insta را بنويس و سپس در کنار ان لينک اينستا بده"

supp = f"جهت پشتيباني به پيوي مراجعه کنيد {support}"

def is_member(user_id):
    try:
        app.get_chat_member(chat_id=channel, user_id=user_id)
        return True
    except:
        return False






#خاموش و روشن
def botstatus(mode):
    global bot1
    bot1 = mode
#مسدود و رفع مسدوديت
def security(method,uid):
    if method == "ban":
        banned.append(int(uid))
    elif method == "unban":
        banned.remove(int(uid))
    else:
        return "method not found"
#سکه  
def coins(method,uid,coin1):
    if method == "addcoin":
        try:
            coinf=open(f"users/{uid}.txt","r")
            usercoin=coinf.readline()
            coinf.close()
            ucoin=int(usercoin)
            ucoin=int(ucoin)+int(coin1)
            scoin=open(f"users/{uid}.txt","w")
            scoin.write(str(ucoin))
            scoin.close()
        except :
            return False
    elif method == "remcoin":
        try:
            coinf=open(f"users/{uid}.txt","r")
            usercoin=coinf.readline()
            coinf.close()
            ucoin=int(usercoin)
            ucoin=int(ucoin)-int(coin1)
            scoin=open(f"users/{uid}.txt","w")
            scoin.write(str(ucoin))
            scoin.close()
        except:
            return False
    else:
        return "method not found"
#سکه دانلود
def downloadcoin(coinpost):
    global coin
    coin = int(coinpost)

def price(toman):
    global coinprice
    coinprice = toman
    
def setofftxt(txt2):
    global offtxt
    offtxt = txt2



def changech(txt):
    global channel
    channel = txt

#از دست زدن در اين قسمت خودداري کنيد   
def coinu(user):
    global coinuser
    coinuser = int(user)
def setstep(status):
    global step
    step = status
def adddown(value):
    global downloads
    downloads = int(downloads)+int(value)




@app.on_message(filters.group & filters.text)
def send_message(app, m:Message):
    try:
        user_id = m.from_user.id
    except AttributeError:
        app.send_message(m.chat.id, text="کاربر گرامي جهت استفاده از ربات بايد حالت ادمين ناشناس را خاموش کنيد",reply_to_message_id=m.id)
    text=m.text
    if bot1 == "on" or user_id == admin and user_id not in banned:
        if text == gp or text == "/start" and user_id not in banned:
            userfile = pathlib.Path(f"users/{user_id}.txt")
            if not userfile.exists():
                fileuser=open(f"users/{user_id}.txt","w")
                fileuser.write("0")
                fileuser.close()
            if is_member(user_id):
                app.send_message(m.chat.id, text=gptxt,reply_to_message_id=m.id)
            else:
                msg=f"کاربر عزیز برای استفاده از ربات لازم است در چنل زیر عضو شوید\n\n{channel}\n{channel}"
                app.send_message(m.chat.id, msg,reply_to_message_id=m.id)
        elif text == "/help" or text == gph and user_id not in banned:
            if is_member(user_id):
                app.send_message(m.chat.id, starthelp, reply_markup=help)
            else:
                msg=f"کاربر عزیز برای استفاده از ربات لازم است در چنل زیر عضو شوید\n\n{channel}\n{channel}"
                app.send_message(m.chat.id, msg,reply_to_message_id=m.id)
        elif text.startswith("insta") and user_id not in banned:
            app.send_message(m.chat.id, "لطفا صبر کنید !",reply_to_message_id=m.id)
            text=text.replace("insta ","")
            coinf=open(f"users/{user_id}.txt","r")
            usercoin=coinf.readline()
            coinf.close()
            ucoin=int(usercoin)
            if ucoin >= coin:
                url=f"https://mrapi.dachhost.top/api/ig.php?url={text}"
                jsoned=requests.get(url)
                js=jsoned.text
                try:
                    adddown("1")
                    ucoin=ucoin-coin
                    scoin=open(f"users/{user_id}.txt","w")
                    scoin.write(str(ucoin))
                    scoin.close()
                    encodejs=json.loads(js)
                    geturl=encodejs["link"]
                    
                    cap="ویدیوی شما دانلود شد"
                    app.send_video(m.chat.id , geturl , caption=cap , reply_to_message_id=m.id)
                except Exception as er:
                    app.send_message(m.chat.id, "درحال حاضر خطايي در ربات رخ داد لطفا دوباره تلاش کنيد يا به پشتيباني اطلاع دهيد\n\nپشتیبانی : ",reply_to_message_id=m.id)
            else:
                app.send_message(m.chat.id, "سکه هاي شما براي دانلود کافي نيست",reply_to_message_id=m.id)
    else:
        app.send_message(m.chat.id, text=offtxt)
                
        

            

@app.on_message(filters.private & filters.text)
def send_message(app, m:Message):
    user_id = m.from_user.id
    text=m.text
    if bot1 == "on" or user_id == admin and user_id not in banned:
        
        if text == "/start" and user_id not in banned:
            userfile = pathlib.Path(f"users/{user_id}.txt")
            if not userfile.exists():
                fileuser=open(f"users/{user_id}.txt","w")
                fileuser.write("0")
                fileuser.close()
            
            if is_member(user_id):
                msg="سلام به ربات اینستا دانلودر خوش امدید جهت دریافت راهنمای عبارت /help را ارسال کنید یا لينک پست خود را ارسال کنید تا ربات شروع به دانلود کردن کند"
                app.send_message(m.chat.id, text=msg,reply_to_message_id=m.id,reply_markup=start_m)
            else:
                msg=f"کاربر عزیز برای استفاده از ربات لازم است در چنل زیر عضو شوید\n\n{channel}\n{channel}"
                app.send_message(m.chat.id, msg,reply_to_message_id=m.id)
        elif text == "/help" or text == "راهنما" and user_id not in banned:
            if is_member(user_id):
                app.send_message(m.chat.id, starthelp, reply_markup=help)
            else:
                msg=f"کاربر عزیز برای استفاده از ربات لازم است در چنل زیر عضو شوید\n\n{channel}\n{channel}"
                app.send_message(m.chat.id, msg,reply_to_message_id=m.id)
        elif text == "/creator" or text == "سازنده" and user_id not in banned:
            if is_member(user_id):
                app.send_message(m.chat.id, "سازنده ربات : میباشد. که توسط زبان برنامه نویسی پایتون این ربات را ساخته است (:")
            else:
                msg=f"کاربر عزیز برای استفاده از ربات لازم است در چنل زیر عضو شوید\n\n{channel}\n{channel}"
                app.send_message(m.chat.id, msg,reply_to_message_id=m.id)
        elif text == "سکه هاي من" and user_id not in banned:
            if is_member(user_id):
                coinfl=open(f"users/{user_id}.txt","r")
                uscoin=coinfl.readline()
                coinfl.close()
                msg=f"سکه هاي شما : {uscoin}"
                app.send_message(m.chat.id, msg)
            else:
                msg=f"کاربر عزیز برای استفاده از ربات لازم است در چنل زیر عضو شوید\n\n{channel}\n{channel}"
                app.send_message(m.chat.id, msg,reply_to_message_id=m.id)
        elif text == "حساب کاربري و آمار" and user_id not in banned:
            if is_member(user_id):
                coinfl1=open(f"users/{user_id}.txt","r")
                uscoin1=coinfl1.readline()
                coinfl1.close()
                msg=f"حساب کاربري شما : \nسکه هاي شما : {uscoin1} \nايدي عددي شما : {user_id}"
                app.send_message(m.chat.id, msg)
            else:
                msg=f"کاربر عزیز برای استفاده از ربات لازم است در چنل زیر عضو شوید\n\n{channel}\n{channel}"
                app.send_message(m.chat.id, msg,reply_to_message_id=m.id)

        elif text == "خريد سکه" and user_id not in banned:
            if is_member(user_id):
                msg=f"برای تهیه سکه در پيوي {support} مراجعه کنید "
                app.send_message(m.chat.id, msg)
            else:
                msg=f"کاربر عزیز برای استفاده از ربات لازم است در چنل زیر عضو شوید\n\n{channel}\n{channel}"
                app.send_message(m.chat.id, msg,reply_to_message_id=m.id)






        #پنل مديريت
        elif text == "panel" and user_id == admin:
            adminmsg="ادمين عزيز به پنل مديريت خوش آمديد"
            app.send_message(m.chat.id, text=adminmsg,reply_markup=keyboard_m)
        elif text == "تنظيمات سکه" and user_id == admin:
            adminmsg="يک گزينه را انتخاب کنيد"
            app.send_message(m.chat.id, text=adminmsg,reply_markup=coin_m)
        elif text == "تنظيمات ربات" and user_id == admin:
            adminmsg="يک گزينه را انتخاب کنيد"
            app.send_message(m.chat.id, text=adminmsg,reply_markup=bot_m)
        elif text == "برگشت به منو اصلي" and user_id == admin:
            adminmsg="به صفحه اصلی برگشتیم"
            app.send_message(m.chat.id, text=adminmsg,reply_markup=keyboard_m)
            
        elif text == "ربات خاموش" and user_id == admin:
            adminmsg="ربات خاموش شد"
            botstatus("off")
            app.send_message(m.chat.id, text=adminmsg,reply_markup=keyboard_m)
        elif text == "ربات روشن" and user_id == admin:
            adminmsg="ربات روشن شد"
            botstatus("on")
            app.send_message(m.chat.id, text=adminmsg,reply_markup=keyboard_m)
            
        elif text == "افزودن سکه به کاربر" and user_id == admin:
            adminmsg="ايدي عددي کاربري که ميخواهيد به آن سکه بدهيد را وارد کنيد"
            setstep("coinid")
            app.send_message(m.chat.id, text=adminmsg,reply_markup=back_m)

        elif text == "رايگان کردن ربات" and user_id == admin:
            adminmsg="جوون من رايگان شدم واسه همه اگه ميخواهي پوليم کني کافيست به پنل بري و در قسمت سکه مورد نياز دانلود پوليم کني"
            downloadcoin("0")
            app.send_message(m.chat.id, text=adminmsg,reply_markup=back_m)

        elif text == "ننظيم سکه مورد نياز پست" and user_id == admin:
            adminmsg="خب پس مخاي پوليم کني حالا بگو از کاربرات براي دانلود چقدر سکه بگيرم؟"
            setstep("setdownloadcoin")
            app.send_message(m.chat.id, text=adminmsg,reply_markup=back_m)
            
        elif text[0].isdigit() and step == "coinid":
            adminmsg="خب حالا مقدار سکه را وارد کن"
            coinu(text)
            setstep("coinamount")
            app.send_message(m.chat.id, text=adminmsg,reply_markup=back_m)
        elif text[0].isdigit() and step == "coinamount":
            status = coins("addcoin",int(coinuser),text)
            if status == False:
                app.send_message(m.chat.id, text="کاربر مورد نظر پيدا نشد",reply_markup=coin_m)
            else:
                adminmsg=f"تعداد {text} سکه به کاربر {coinuser} هديه داده شد"
                app.send_message(m.chat.id, text=adminmsg,reply_markup=coin_m)
                usermsg=f"شما از طرف مديريت {text} سکه دريافت کرديد"
                app.send_message(coinuser, text=usermsg)
                
            setstep("none")
        #post
            
        elif text == "تنطيم سکه مورد نياز پست" and user_id == admin:
            adminmsg="دوست داري براي هر دانلود چقدر سکه بگيرم؟"
            setstep("setdownloadcoin")
            app.send_message(m.chat.id, text=adminmsg,reply_markup=back_m)
        elif text[0].isdigit() and step == "setdownloadcoin":
            downloadcoin(text)
            adminmsg=f"من پولي شدم از اين بع بعد از کاربر ها {text} سکه براي هر دانلود ميگيرم"
            app.send_message(m.chat.id, text=adminmsg,reply_markup=coin_m)
                
            setstep("none")
        #price
        elif text == "تعيين قيمت سکه" and user_id == admin:
            adminmsg="دوست داري قيمت سکه ام چند باشه؟ به روپیه لطفا"
            setstep("setpricecoin")
            app.send_message(m.chat.id, text=adminmsg,reply_markup=back_m)
            
            
        elif text[0].isdigit() and step == "setpricecoin":
            adminmsg=f"قيمت سکه به {text} روپیه تغيير يافت"
            price(text)
            app.send_message(m.chat.id, text=adminmsg,reply_markup=coin_m)
            setstep("none")

        #offtxt
        elif text == "تنظيم متن خاموشي" and user_id == admin:
            adminmsg="متن خاموشي را بفرستيد"
            setstep("setofftxt")
            app.send_message(m.chat.id, text=adminmsg,reply_markup=back_m)
            
        elif step == "setofftxt":
            adminmsg=f"متن خاموشي تغيير يافت متن جديد : \n{text}"
            setofftxt(text)
            app.send_message(m.chat.id, text=adminmsg,reply_markup=bot_m)
            setstep("none")

        

        #ch
        elif text == "تغيير چنل جوين اجباري" and user_id == admin:
            adminmsg="ايدي جديد چنل را با @ بفرستيد"
            setstep("setchid")
            app.send_message(m.chat.id, text=adminmsg,reply_markup=back_m)
            
        elif step == "setchid":
            adminmsg=f"ايدي چنل جوين اجباري به {text} تغيير يافت"
            changech(text)
            app.send_message(m.chat.id, text=adminmsg,reply_markup=bot_m)
            setstep("none")


        #ban
        elif text == "مسدود کردن فرد" and user_id == admin:
            adminmsg="ايدي عددي فرد مجرم رو بده تا مسدودش کنم تا از اين کارا نکنه"
            setstep("banuser")
            app.send_message(m.chat.id, text=adminmsg,reply_markup=back_m)
            
        elif text[0].isdigit() and step == "banuser":
            adminmsg=f"فرد مجرم {text} ديگه نميتونه از ربات استفاده کنه"
            security("ban",int(text))
            app.send_message(m.chat.id, text=adminmsg,reply_markup=keyboard_m)
            app.send_message(m.chat.id, text=str(banned),reply_markup=keyboard_m)
            setstep("none")

        #unban
        elif text == "رفع مسدود کردن فرد" and user_id == admin:
            adminmsg="جونم رييس ايدي عددي زنداني رو بده تا ازادش کنم"
            setstep("unbanuser")
            app.send_message(m.chat.id, text=adminmsg,reply_markup=back_m)
            
        elif text[0].isdigit() and step == "unbanuser":
            adminmsg=f"زنداني {text} ديگه ميتونه از ربات استفاده کنه"
            security("unban",int(text))
            app.send_message(m.chat.id, text=adminmsg,reply_markup=keyboard_m)
            setstep("none")

        
        #remcoin
        elif text == "کسر سکه از کاربر" and user_id == admin:
            adminmsg="ايدي عددي فردي که ميخواهيد از او سکه بگيريد را وارد کنيد"
            setstep("coinidrem")
            app.send_message(m.chat.id, text=adminmsg,reply_markup=back_m)
        elif text[0].isdigit() and step == "coinidrem":
            adminmsg="خب حالا مقدار سکه را وارد کن"
            coinu(text)
            setstep("coinamountrem")
            app.send_message(m.chat.id, text=adminmsg,reply_markup=back_m)
        elif text[0].isdigit() and step == "coinamountrem":
            status = coins("remcoin",int(coinuser),text)
            if status == False:
                app.send_message(m.chat.id, text="کاربر مورد نظر پيدا نشد",reply_markup=coin_m)
            else:
                adminmsg=f"تعداد {text} سکه به کاربر {coinuser} کسر شد"
                app.send_message(m.chat.id, text=adminmsg,reply_markup=coin_m)
                usermsg=f"شما از طرف مديريت {text} سکه از دست داديد"
                app.send_message(coinuser, text=usermsg)
                
            setstep("none")
        elif text == "آمار ربات" and user_id == admin:
            members = len(fnmatch.filter(os.listdir("users"), '*.txt'))
            adminmsg=f"آمار ربات عبارت است از \n تعداد دانلود ها : {downloads}\nکاربران ربات : {members}"
            app.send_message(m.chat.id, text=adminmsg,reply_markup=keyboard_m)

        elif text.startswith("https://www.instagram.com") or text.startswith("https://instagram.com") or text.startswith("https://in") and user_id not in banned:
            coinf = open(f"users/{user_id}.txt", "r")
            usercoin=coinf.readline()
            coinf.close()
            ucoin=int(usercoin)
            if ucoin >= coin:
                app.send_message(m.chat.id, "لطفا صبر کنید !",reply_to_message_id=m.id)
                url=f"https://mrapi.dachhost.top/api/ig.php?url={text}"
                jsoned=requests.get(url)
                js=jsoned.text
                try:
                    adddown("1")
                    ucoin=ucoin-coin
                    scoin=open(f"users/{user_id}.txt","w")
                    scoin.write(str(ucoin))
                    scoin.close()
                    encodejs=json.loads(js)
                    geturl=encodejs["link"]
                    
                    cap="ویدیوی شما دانلود شد"
                    app.send_video(m.chat.id , geturl , caption=cap , reply_to_message_id=m.id)
                except Exception as er:
                    app.send_message(m.chat.id, "درحال حاضر خطايي در ربات رخ داد لطفا دوباره تلاش کنيد يا به پشتيباني اطلاع دهيد\n\nپشتیبانی : ",reply_to_message_id=m.id)
            else:
                app.send_message(m.chat.id, "سکه هاي شما براي دانلود کافي نيست",reply_to_message_id=m.id)
        #if step == "coinadd":
            #addcoin(text)
    else:
        app.send_message(m.chat.id, text=offtxt)
        


@app.on_callback_query()
def test(app, call):
    message = call.message
    if call.data == "back":
        call.edit_message_text(starthelp, reply_markup=help)
                  
    elif call.data == "dhelp":
        call.edit_message_text(text=helptxt , reply_markup=add)
         
    elif call.data == "supp":
        call.edit_message_text(text=supp , reply_markup=gpbtn)

    elif call.data == "close":
        call.edit_message_text(text="پنل راهنما با موفقیت بسته شد")
    


app.run()


#=================================
#ساخته شده توسط @sourcemr
#کپی برداری بدون ذکر منبع حرام میباشد
#اگه دوست داری سر پل صراط جلوتو نگیرم منبع رو پاک نکن
#=================================
