import logging
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import requests
import re
import uuid
import string
import random
import base64
from datetime import datetime
import asyncio

# تفعيل السجل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# المراحل
(MENU, SESSION_CHOICE, SESSION_INPUT, USERNAME_INPUT, PASSWORD_INPUT, 
 TARGET_INPUT, REPORT_TYPE) = range(7)

# التحقق من تاريخ الصلاحية
def check_date():
    current_date = datetime.now().date()
    target_date = datetime(2025, 12, 1, 23, 59, 59).date()
    if current_date >= target_date:
        return False
    return True

# التحقق من صلاحية الـ session
def verify_session(sessionid):
    try:
        session = requests.Session()
        session.cookies.set('sessionid', sessionid, domain='.instagram.com')
        
        r = session.get('https://www.instagram.com/accounts/edit/',
                       headers={
                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
                       },
                       timeout=30)
        
        if r.status_code == 200 and 'login' not in r.url:
            try:
                csrftoken = r.cookies.get('csrftoken')
                if not csrftoken:
                    csrftoken_match = re.search(r'"csrf_token":"([^"]+)"', r.text)
                    if csrftoken_match:
                        csrftoken = csrftoken_match.group(1)
                
                return True, csrftoken
            except:
                return False, None
        else:
            return False, None
    except Exception as e:
        logger.error(f"Error verifying session: {e}")
        return False, None

# استخراج الـ Session ID
def extract_sessionid(user, password):
    try:
        my_uuid = uuid.uuid4()
        my_uuid_str = str(my_uuid)
        modified_uuid_str = my_uuid_str[:8] + "should_trigger_override_login_success_action" + my_uuid_str[8:]
        rd = ''.join(random.choices(string.ascii_lowercase+string.digits, k=16))
        
        data = {"params": "{\"client_input_params\":{\"contact_point\":\"" + user + "\",\"password\":\"#PWD_INSTAGRAM:0:0:" +  password + "\",\"fb_ig_device_id\":[],\"event_flow\":\"login_manual\",\"openid_tokens\":{},\"machine_id\":\"ZG93WAABAAEkJZWHLdW_Dm4nIE9C\",\"family_device_id\":\"\",\"accounts_list\":[],\"try_num\":1,\"login_attempt_count\":1,\"device_id\":\"android-" + rd + "\",\"auth_secure_device_id\":\"\",\"device_emails\":[],\"secure_family_device_id\":\"\",\"event_step\":\"home_page\"},\"server_params\":{\"is_platform_login\":0,\"qe_device_id\":\"\",\"family_device_id\":\"\",\"credential_type\":\"password\",\"waterfall_id\":\"" + modified_uuid_str + "\",\"username_text_input_id\":\"9cze54:46\",\"password_text_input_id\":\"9cze54:47\",\"offline_experiment_group\":\"caa_launch_ig4a_combined_60_percent\",\"INTERNAL__latency_qpl_instance_id\":56600226400306,\"INTERNAL_INFRA_THEME\":\"default\",\"device_id\":\"android-" + ''.join(random.choices(string.ascii_lowercase+string.digits, k=16)) + "\",\"server_login_source\":\"login\",\"login_source\":\"Login\",\"should_trigger_override_login_success_action\":0,\"ar_event_source\":\"login_home_page\",\"INTERNAL__latency_qpl_marker_id\":36707139}}"}
        data["params"] = data["params"].replace("\"family_device_id\":\"\"", "\"family_device_id\":\"" +my_uuid_str + "\"")
        data["params"] = data["params"].replace("\"qe_device_id\":\"\"", "\"qe_device_id\":\"" + my_uuid_str + "\"")
        
        headers = {"Host": "i.instagram.com","X-Ig-App-Locale": "ar_SA","X-Ig-Device-Locale": "ar_SA","X-Ig-Mapped-Locale": "ar_AR","X-Pigeon-Session-Id": f"UFS-{uuid.uuid4()}-0","X-Pigeon-Rawclienttime": "1685026670.130","X-Ig-Bandwidth-Speed-Kbps": "-1.000","X-Ig-Bandwidth-Totalbytes-B": "0","X-Ig-Bandwidth-Totaltime-Ms": "0","X-Bloks-Version-Id": "8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb","X-Ig-Www-Claim": "0","X-Bloks-Is-Layout-Rtl": "true","X-Ig-Device-Id": f"{uuid.uuid4()}","X-Ig-Family-Device-Id": f"{uuid.uuid4()}","X-Ig-Android-Id": f"android-{''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}","X-Ig-Timezone-Offset": "10800","X-Fb-Connection-Type": "WIFI","X-Ig-Connection-Type": "WIFI","X-Ig-Capabilities": "3brTv10=","X-Ig-App-Id": "567067343352427","Priority": "u=3","User-Agent": f"Instagram 303.0.0.0.59 Android (28/9; 320dpi; 900x1600; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}/{''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; en_GB;)","Accept-Language": "ar-SA, en-US","Ig-Intended-User-Id": "0","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Content-Length": "1957","Accept-Encoding": "gzip, deflate","X-Fb-Http-Engine": "Liger","X-Fb-Client-Ip": "True","X-Fb-Server-Cluster": "True"}
        
        response = requests.post('https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.login.async.send_login_request/',
                                headers=headers, 
                                data=data,
                                timeout=30)
        body = response.text
        
        if "Bearer" in body:
            session = re.search(r'Bearer IGT:2:(.*?),',response.text).group(1).strip()
            session = session[:-8]
            full=base64.b64decode(session).decode('utf-8')
            if "sessionid"  in full:
                sessionid = re.search(r'"sessionid":"(.*?)"}',full).group(1).strip()
                return sessionid, None
        elif "The password you entered is incorrect" in body or "Please check your username and try again." in body or "inactive user" in body or "should_dismiss_loading\", \"has_identification_error\"" in body:
            return None, "كلمة المرور خاطئة"
        elif "challenge_required" in body or "two_step_verification" in body:
            return None, "يتطلب تحدي - الرجاء قبول التحدي والمحاولة مرة أخرى"
        else:
            return None, "حدث خطأ ما"
    except Exception as e:
        logger.error(f"Error extracting session: {e}")
        return None, f"خطأ في الاتصال: {str(e)}"

# الحصول على ID الهدف
def get_target_id(target, sessionid, csrftoken):
    try:
        r2 = requests.post('https://i.instagram.com:443/api/v1/users/lookup/',
                 headers={
                     "Connection": "close",
                     "X-IG-Connection-Type": "WIFI",
                     "mid": "XOSINgABAAG1IDmaral3noOozrK0rrNSbPuSbzHq",
                     "X-IG-Capabilities": "3R4=",
                     "Accept-Language": "ar-sa",
                     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                     "User-Agent": "Instagram 99.4.0 TweakPY_vv1ck (TweakPY_vv1ck)",
                     "Accept-Encoding": "gzip, deflate",
                     "Cookie": f"sessionid={sessionid}"
                 },
                 data={"signed_body": "35a2d547d3b6ff400f713948cdffe0b789a903f86117eb6e2f3e573079b2f038.{\"q\":\"%s\"}" % target},
                 timeout=30)
        
        if 'No users found' in r2.text:
            adv_search = requests.get(f'https://www.instagram.com/{target}',
                            headers={
                                'Host': 'www.instagram.com',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                                'Accept-Language': 'ar,en-US;q=0.7,en;q=0.3',
                                'Accept-Encoding': 'gzip, deflate, br',
                                'Connection': 'keep-alive',
                                'Cookie': f'csrftoken={csrftoken}; sessionid={sessionid}',
                                'Upgrade-Insecure-Requests': '1',
                                'Sec-Fetch-Dest': 'document',
                                'Sec-Fetch-Mode': 'navigate',
                                'Sec-Fetch-Site': 'none',
                                'Sec-Fetch-User': '?1',
                                'TE': 'trailers'
                            },
                            timeout=30)
            try:
                target_id = re.findall('"profile_id":"(.*?)"', adv_search.text)[0]
                return target_id, None
            except IndexError:
                try:
                    target_id = re.findall('"page_id":"profilePage_(.*?)"', adv_search.text)[0]
                    return target_id, None
                except IndexError:
                    try:
                        adv_search2 = requests.get(f'https://www.instagram.com/api/v1/users/web_profile_info/?username={target}',
                                         headers={
                                             'Host': 'www.instagram.com',
                                             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
                                             'Accept': '*/*',
                                             'Accept-Language': 'ar,en-US;q=0.7,en;q=0.3',
                                             'Accept-Encoding': 'gzip, deflate, br',
                                             'X-CSRFToken': csrftoken,
                                             'X-IG-App-ID': '936619743392459',
                                             'X-ASBD-ID': '198387',
                                             'X-IG-WWW-Claim': 'hmac.AR3KPEPoXkWYhwtoCUKyUHK80GsE1g2PJI1uPtDlCyo4PHKn',
                                             'X-Requested-With': 'XMLHttpRequest',
                                             'Alt-Used': 'www.instagram.com',
                                             'Connection': 'keep-alive',
                                             'Referer': f'https://www.instagram.com/{target}/',
                                             'Cookie': f'sessionid={sessionid}; csrftoken={csrftoken}',
                                             'Sec-Fetch-Dest': 'empty',
                                             'Sec-Fetch-Mode': 'cors',
                                             'Sec-Fetch-Site': 'same-origin',
                                             'TE': 'trailers'
                                         },
                                         timeout=30)
                        target_id = adv_search2.json()['data']['user']['id']
                        return target_id, None
                    except KeyError:
                        return None, "فشل في الحصول على ID الهدف"
        elif '"spam":true' in r2.text:
            return None, "حاول مرة أخرى لاحقاً"
        else:
            try:
                target_id = str(r2.json()['user_id'])
                return target_id, None
            except KeyError:
                return None, "خطأ عام"
    except Exception as e:
        logger.error(f"Error getting target ID: {e}")
        return None, f"خطأ في الاتصال: {str(e)}"

# إرسال البلاغ
def send_report(target_id, sessionid, csrftoken, report_type):
    try:
        r3 = requests.post("https://i.instagram.com/users/"+target_id+"/flag/",
                          headers={
                              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
                              "Host": "i.instagram.com",
                              'cookie': f"sessionid={sessionid}",
                              "X-CSRFToken": csrftoken,
                              "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                          },
                          data=f'source_name=&reason_id={report_type}&frx_context=',
                          allow_redirects=False,
                          timeout=30)
        
        if r3.status_code == 429:
            return False, f"تم حظرك - كود الحالة [{r3.status_code}]"
        elif r3.status_code == 500:
            return False, f"الهدف غير موجود - كود الحالة [{r3.status_code}]"
        else:
            return True, f"تم إرسال البلاغ بنجاح - كود الحالة [{r3.status_code}]"
    except requests.exceptions.TooManyRedirects:
        return True, f"تم إرسال البلاغ بنجاح"
    except Exception as e:
        logger.error(f"Error sending report: {e}")
        return False, f"فشل البلاغ: {str(e)}"

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_date():
        await update.message.reply_text(
            "انتهت صلاحية الأداة.\n"
            "للتجديد، تواصل مع:\n"
            "Instagram: @g2z.9\n"
            "Telegram: @aazzaarrdd"
        )
        return ConversationHandler.END
    
    # رسالة الترحيب والشرح
    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "      مرحباً بك في بوت Instagram Report\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "المطور: azard & slax\n"
        "Telegram: @aazzaarrdd\n"
        "Instagram: @g2z.9\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "      ماذا يمكن لهذا البوت فعله؟\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "هذا البوت يساعدك في:\n\n"
        "1. إرسال بلاغات متعددة لحسابات Instagram\n"
        "2. يدعم 22 نوع من البلاغات\n"
        "3. يمكنك استخراج Session ID تلقائياً\n"
        "4. إرسال بلاغات مستمرة حتى الإيقاف\n"
        "5. متابعة عدد البلاغات المرسلة\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "      أنواع البلاغات المتاحة:\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "1 - Spam (سبام)\n"
        "2 - Self Injury (إيذاء النفس و إنتحار)\n"
        "3 - Sale (بيع مخدرات)\n"
        "4 - Nudity (محتوى إباحي)\n"
        "5 - Violence (عنف ومنظمات خطرة)\n"
        "6 - Hate  (خطاب كراهية)\n"
        "7 - Harassment (مضايقة)\n"
        "8 - instagram (انتحال إنستا)\n"
        "9 - instagram business (إنتحال إنستا الاعمال)\n"
        "10- Copyright (إنتحال قسم دعم كوبيرايت)\n"
        "11 - Nudity kids (قاصر)\n"
        "12 - arms sale (بيع أسلحة)\n"
        "13 - violence (عنف عشوائي)\n"
        "14 - violence (عنف عشوائي)\n"
        "15 - violence (عنف عشوائي)\n"
        "16 - sale illegal (بيع غير قانوني~مختلف عن المخدرات)\n"
        "17 - violence (عشوائي)\n"
        "18 - violence (عشوائي)\n"
        "19 - violence (عشوائي)\n"
        "20- violence (افراد خطرون ومنظمات خطرة~مختلف عن رقم 5)\n"
        "21 - violence (عشوائي)\n"
        "22 - data & people (تداخل بيانات الناخبين او تعداد السكان)\n"
        
        
        "- \n"
        "- وغيرها...\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "      الأوامر المتاحة:\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "/start - بدء البوت\n"
        "/stop - إيقاف البلاغات\n"
        "/cancel - إلغاء العملية الحالية\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "الآن، لنبدأ!"
    )
    
    await asyncio.sleep(1)
    
    keyboard = [
        ['استخراج Session ID'],
        ['إدخال Session ID يدوياً']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "اختر طريقة تسجيل الدخول:",
        reply_markup=reply_markup
    )
    
    return SESSION_CHOICE

async def session_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    
    if choice == 'استخراج Session ID':
        await update.message.reply_text(
            "أدخل اسم المستخدم الخاص بك:",
            reply_markup=ReplyKeyboardRemove()
        )
        return USERNAME_INPUT
    else:
        await update.message.reply_text(
            "أدخل Session ID الخاص بك:",
            reply_markup=ReplyKeyboardRemove()
        )
        return SESSION_INPUT

async def username_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['username'] = update.message.text
    await update.message.reply_text("أدخل كلمة المرور:")
    return PASSWORD_INPUT

async def password_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = context.user_data['username']
    password = update.message.text
    
    await update.message.reply_text("جاري استخراج Session ID...")
    
    sessionid, error = extract_sessionid(username, password)
    
    if sessionid:
        context.user_data['sessionid'] = sessionid
        is_valid, csrftoken = verify_session(sessionid)
        if is_valid:
            context.user_data['csrftoken'] = csrftoken
            await update.message.reply_text(
                f"تم تسجيل الدخول بنجاح!\n\n"
                f"Session ID:\n{sessionid}\n\n"
                f"أدخل اسم المستخدم المستهدف:"
            )
            return TARGET_INPUT
        else:
            await update.message.reply_text("Session ID غير صالح. /start للبدء من جديد")
            return ConversationHandler.END
    else:
        await update.message.reply_text(f"خطأ: {error}\n\n/start للبدء من جديد")
        return ConversationHandler.END

async def session_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sessionid = update.message.text.strip()
    
    if not sessionid:
        await update.message.reply_text("يجب إدخال Session ID!\n/start للبدء من جديد")
        return ConversationHandler.END
    
    await update.message.reply_text("جاري التحقق من Session ID...")
    
    is_valid, csrftoken = verify_session(sessionid)
    
    if is_valid:
        context.user_data['sessionid'] = sessionid
        context.user_data['csrftoken'] = csrftoken
        await update.message.reply_text(
            "تم التحقق بنجاح!\n\n"
            "أدخل اسم المستخدم المستهدف:"
        )
        return TARGET_INPUT
    else:
        await update.message.reply_text(
            "Session ID غير صالح أو منتهي الصلاحية!\n"
            "/start للبدء من جديد"
        )
        return ConversationHandler.END

async def target_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.message.text.strip().replace('@', '')
    context.user_data['target'] = target
    
    await update.message.reply_text("جاري البحث عن الهدف...")
    
    sessionid = context.user_data['sessionid']
    csrftoken = context.user_data['csrftoken']
    
    target_id, error = get_target_id(target, sessionid, csrftoken)
    
    if target_id:
        context.user_data['target_id'] = target_id
        
        keyboard = [
            ['1 - Spam', '2 - Self'],
            ['3 - Sale', '4 - Nudity'],
            ['5 - Violence+dangerous organization', '6 - Hate'],
            ['7 - Harassment', '8 - Instagram'],
            ['9 - Instagram Business', '10 - Copyright'],
            ['11 - kids(-18)', '12 - sale arms'],
            ['13 - (?)', '14 - violence'],
            ['15 - Violence 1' , '16 - sale illegal '],
            ['17 - violence' , '18 - violence'],
            ['19 - violence' , '20 - dangerous people+dangerous organization'],
            ['21 - None','22 - data & people'],

            
            
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            f"تم العثور على الهدف!\n"
            f"ID: {target_id}\n\n"
            f"اختر نوع البلاغ:",
            reply_markup=reply_markup
        )
        return REPORT_TYPE
    else:
        await update.message.reply_text(
            f"خطأ: {error}\n"
            "/start للبدء من جديد"
        )
        return ConversationHandler.END

# متغير عام لتخزين المهمة الحالية
active_tasks = {}

async def reporting_task(update: Update, context: ContextTypes.DEFAULT_TYPE, target_id, target, sessionid, csrftoken, report_type):
    """مهمة منفصلة لإرسال البلاغات"""
    user_id = update.effective_user.id
    count = 0
    success_count = 0
    fail_count = 0
    start_time = datetime.now()
    
    try:
        while user_id in active_tasks and active_tasks[user_id]:
            success, message = send_report(target_id, sessionid, csrftoken, report_type)
            count += 1
            
            if success:
                success_count += 1
                if count % 5 == 0:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"━━━━━━━━━━━━━━━━━━━━━━\n"
                             f"      تحديث البلاغات\n"
                             f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                             f"تم إرسال: {success_count} بلاغ ناجح\n"
                             f"فشل: {fail_count} بلاغ\n"
                             f"المجموع: {count} محاولة\n\n"
                             f"البلاغات مستمرة...\n"
                             f"للإيقاف: /stop"
                    )
            else:
                fail_count += 1
                if "حظرك" in message or "429" in message:
                    end_time = datetime.now()
                    duration = end_time - start_time
                    
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"━━━━━━━━━━━━━━━━━━━━━━\n"
                             f"      تقرير نهائي\n"
                             f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                             f"تم إيقاف البلاغات\n\n"
                             f"السبب: {message}\n\n"
                             f"الإحصائيات:\n"
                             f"━━━━━━━━━━━━━━━━━━━━━━\n"
                             f"البلاغات الناجحة: {success_count}\n"
                             f"البلاغات الفاشلة: {fail_count}\n"
                             f"المجموع الكلي: {count}\n\n"
                             f"الهدف: @{target}\n"
                             f"نوع البلاغ: {report_type}\n"
                             f"المدة: {duration.seconds} ثانية\n\n"
                             f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                             f"/start للبدء من جديد"
                    )
                    break
            
            # تأخير بين كل بلاغ (2 ثانية) مع فحص الإيقاف كل 0.5 ثانية
            for _ in range(4):
                if user_id not in active_tasks or not active_tasks[user_id]:
                    break
                await asyncio.sleep(0.5)
        
        # إذا تم الإيقاف يدوياً
        if user_id not in active_tasks or not active_tasks[user_id]:
            end_time = datetime.now()
            duration = end_time - start_time
            
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"━━━━━━━━━━━━━━━━━━━━━━\n"
                     f"      تقرير نهائي\n"
                     f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                     f"تم إيقاف البلاغات يدوياً\n\n"
                     f"الإحصائيات:\n"
                     f"━━━━━━━━━━━━━━━━━━━━━━\n"
                     f"البلاغات الناجحة: {success_count}\n"
                     f"البلاغات الفاشلة: {fail_count}\n"
                     f"المجموع الكلي: {count}\n\n"
                     f"الهدف: @{target}\n"
                     f"نوع البلاغ: {report_type}\n"
                     f"المدة: {duration.seconds} ثانية\n\n"
                     f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                     f"/start للبدء من جديد"
            )
    except Exception as e:
        logger.error(f"Error in reporting task: {e}")
    finally:
        if user_id in active_tasks:
            del active_tasks[user_id]

async def report_type_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    
    try:
        report_type = int(choice.split('-')[0].strip())
        if report_type < 1 or report_type > 22:
            await update.message.reply_text("رقم غير صحيح! اختر من 1 إلى 22")
            return REPORT_TYPE
    except:
        await update.message.reply_text("رقم غير صحيح! اختر من القائمة")
        return REPORT_TYPE
    
    target_id = context.user_data['target_id']
    target = context.user_data['target']
    sessionid = context.user_data['sessionid']
    csrftoken = context.user_data['csrftoken']
    user_id = update.effective_user.id
    
    await update.message.reply_text(
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"      بدء عملية الإبلاغ\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"الهدف: @{target}\n"
        f"ID: {target_id}\n"
        f"نوع البلاغ: {report_type}\n\n"
        f"جاري إرسال البلاغات...\n\n"
        f"للإيقاف في أي وقت، اضغط /stop",
        reply_markup=ReplyKeyboardRemove()
    )
    
    # بدء مهمة البلاغات في الخلفية
    active_tasks[user_id] = True
    asyncio.create_task(reporting_task(update, context, target_id, target, sessionid, csrftoken, report_type))
    
    return ConversationHandler.END

async def stop_reporting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id in active_tasks and active_tasks[user_id]:
        active_tasks[user_id] = False
        await update.message.reply_text(
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "      تم الإيقاف\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "جاري إيقاف البلاغات...\n"
            "انتظر قليلاً لرؤية التقرير النهائي"
        )
    else:
        await update.message.reply_text(
            "لا توجد عملية إبلاغ جارية حالياً.\n\n"
            "/start للبدء من جديد"
        )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "تم إلغاء العملية.\n"
        "/start للبدء من جديد",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Exception while handling an update: {context.error}")

def main():
    # توكن البوت
    TOKEN = "8430539370:AAH1u6Z1b_V-6t7pQjBEsBvwHu4lcjY6Yv0"
    
    # إنشاء التطبيق
    application = Application.builder().token(TOKEN).build()
    
    # إضافة معالج الأوامر العامة أولاً
    application.add_handler(CommandHandler('stop', stop_reporting))
    
    # إضافة معالج المحادثة
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SESSION_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, session_choice)],
            USERNAME_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, username_input)],
            PASSWORD_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, password_input)],
            SESSION_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, session_input)],
            TARGET_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, target_input)],
            REPORT_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, report_type_selection)],
        },
        fallbacks=[
            CommandHandler('cancel', cancel)
        ],
    )
    
    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)
    
    # تشغيل البوت
    logger.info("البوت يعمل الآن...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
