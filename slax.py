from requests import post, get
import requests, os, re, uuid, string, random, base64
from datetime import datetime   

try:
    import requests
except:
    os.system("pip install requests")    

try:
    from rich.console import Console
except:
    os.system("pip install rich")

    
        

                                        
    

def check_date():
    current_date = datetime.now().date()
    target_date = datetime(2025, 12, 1, 23, 59, 59).date()
    if current_date >= target_date:
        print("""The tool's validity has expired.
To renew, please contact instagram : @g2z.9 or telegram : aazzaarrdd . """)
        exit()
check_date()




mag = "\033[1m\033[35m"
g= "\033[1m\033[32m"
y= "\033[1m\033[33m"
red = "\033[1m\033[31m"
green = "\033[1m\033[32m"
yellow = "\033[1m\033[33m"
blue = "\033[1m\033[34m"
cyan = "\033[1m\033[36m"
magenta = "\033[1m\033[35m"
M = "\033[1m\033[36m"
white = "\033[1m\033[37m"
orange = "\033[1m\033[38;5;208m"
reset = "\033[0m"
org = "\033[1m\033[38;5;208m"

uid=str(uuid.uuid4())
console=Console()

def header():
    os.system("cls" if os.name=='nt' else "clear")
    print( """

 █████╗ ███████╗ █████╗ ██████╗ ██████╗     
██╔══██╗╚══███╔╝██╔══██╗██╔══██╗██╔══██╗    
███████║  ███╔╝ ███████║██████╔╝██║  ██║    
██╔══██║ ███╔╝  ██╔══██║██╔══██╗██║  ██║    
██║  ██║███████╗██║  ██║██║  ██║██████╔╝    
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝       
         
the tool by azard & slax

TLE : aazzaarrdd 

INSTA : slax - @g2z.9


  """
  
  )
    console.print(f"""
Bot Spam coded by @g2z.9 - TLE:@aazzaarrdd
bot Instagram ~ slax (@g2z.9)
""",style='bold purple4',justify='left')
    print("")

def Report_Instagram(target_id,sessionid,csrftoken):
    header()
    
    print(f"""
{cyan} _____________________________
|                             | 
| {y}~${mag} choose the report{cyan}        |
|_____________________________|

------------------------------
| {g}1 ~ {y}spam {cyan}                  |
------------------------------
| {g}2 ~ {y}self {cyan}                  |
------------------------------
| {g}3 ~ {y}sale {cyan}                  |
------------------------------
| {g}4 ~ {y}Nudity {cyan}              |
------------------------------
| {g}5 ~ {y}violence {cyan}              |
------------------------------
| {g}6 ~ {y}hate {cyan}                  |
------------------------------
| {g}7 ~ {y}harassment {cyan}            |
------------------------------
| {g}8 ~ {y}instagram {cyan}             |
------------------------------
| {g}9 ~ {y}instagram business {cyan}    |
------------------------------
| {g}10 ~ {y}copyright {cyan}            |
------------------------------
| {g}11 ~ {y}Impression 3 business{cyan}                  |
------------------------------
| {g}12 ~ {y}Impression 3 instagram {cyan}                  |
------------------------------
| {g}13 ~ {y}Impression 4 business {cyan}                   |
------------------------------
| {g}14 ~ {y}Impression 4 instagram {cyan}                  |
------------------------------
| {g}15 ~ {y}Violence 1 {cyan}               |
------------------------------
""")

    try:
        reportType = int(input("-> type number (1-15): "))
        if reportType > 15 or reportType < 1:
            print("wrong number\ntry again")
        else:
            print(f"You chose report type {reportType}.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    
    while 1:
        try:
            r3=post("https://i.instagram.com/users/"+target_id+"/flag/",headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0","Host": "i.instagram.com",'cookie': f"sessionid={sessionid}","X-CSRFToken": csrftoken,"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},data=f'source_name=&reason_id={reportType}&frx_context=',allow_redirects=False)
            if r3.status_code==429:
                console.print(f"- Ban with status code [ {r3.status_code} ] ");exit()
            elif r3.status_code==500:
                console.print(f"- Target Not Found with status code [ {r3.status_code} ] ");exit()
            else:
                console.print(f"- Report Done with status code [ {r3.status_code} ] ") 				
        except requests.exceptions.TooManyRedirects:
            console.print(f"- Report Done with status code [ {r3.status_code} ] ")
        except Exception as e:
            console.print(f"- Report Failed with status code [ {r3.status_code} ] ");exit()

def verify_session(sessionid):
    """التحقق من صلاحية الـ session"""
    try:
        session = requests.Session()
        session.cookies.set('sessionid', sessionid, domain='.instagram.com')
        
        r = session.get('https://www.instagram.com/accounts/edit/',
                       headers={
                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
                       })
        
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
        return False, None

def extract_sessionid(user, password):
    """استخراج الـ Session ID من Username و Password"""
    my_uuid = uuid.uuid4()
    my_uuid_str = str(my_uuid)
    modified_uuid_str = my_uuid_str[:8] + "should_trigger_override_login_success_action" + my_uuid_str[8:]
    rd = ''.join(random.choices(string.ascii_lowercase+string.digits, k=16))
    
    data = {"params": "{\"client_input_params\":{\"contact_point\":\"" + user + "\",\"password\":\"#PWD_INSTAGRAM:0:0:" +  password + "\",\"fb_ig_device_id\":[],\"event_flow\":\"login_manual\",\"openid_tokens\":{},\"machine_id\":\"ZG93WAABAAEkJZWHLdW_Dm4nIE9C\",\"family_device_id\":\"\",\"accounts_list\":[],\"try_num\":1,\"login_attempt_count\":1,\"device_id\":\"android-" + rd + "\",\"auth_secure_device_id\":\"\",\"device_emails\":[],\"secure_family_device_id\":\"\",\"event_step\":\"home_page\"},\"server_params\":{\"is_platform_login\":0,\"qe_device_id\":\"\",\"family_device_id\":\"\",\"credential_type\":\"password\",\"waterfall_id\":\"" + modified_uuid_str + "\",\"username_text_input_id\":\"9cze54:46\",\"password_text_input_id\":\"9cze54:47\",\"offline_experiment_group\":\"caa_launch_ig4a_combined_60_percent\",\"INTERNAL__latency_qpl_instance_id\":56600226400306,\"INTERNAL_INFRA_THEME\":\"default\",\"device_id\":\"android-" + ''.join(random.choices(string.ascii_lowercase+string.digits, k=16)) + "\",\"server_login_source\":\"login\",\"login_source\":\"Login\",\"should_trigger_override_login_success_action\":0,\"ar_event_source\":\"login_home_page\",\"INTERNAL__latency_qpl_marker_id\":36707139}}"}
    data["params"] = data["params"].replace("\"family_device_id\":\"\"", "\"family_device_id\":\"" +my_uuid_str + "\"")
    data["params"] = data["params"].replace("\"qe_device_id\":\"\"", "\"qe_device_id\":\"" + my_uuid_str + "\"")
    
    headers = {"Host": "i.instagram.com","X-Ig-App-Locale": "ar_SA","X-Ig-Device-Locale": "ar_SA","X-Ig-Mapped-Locale": "ar_AR","X-Pigeon-Session-Id": f"UFS-{uuid.uuid4()}-0","X-Pigeon-Rawclienttime": "1685026670.130","X-Ig-Bandwidth-Speed-Kbps": "-1.000","X-Ig-Bandwidth-Totalbytes-B": "0","X-Ig-Bandwidth-Totaltime-Ms": "0","X-Bloks-Version-Id": "8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb","X-Ig-Www-Claim": "0","X-Bloks-Is-Layout-Rtl": "true","X-Ig-Device-Id": f"{uuid.uuid4()}","X-Ig-Family-Device-Id": f"{uuid.uuid4()}","X-Ig-Android-Id": f"android-{''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}","X-Ig-Timezone-Offset": "10800","X-Fb-Connection-Type": "WIFI","X-Ig-Connection-Type": "WIFI","X-Ig-Capabilities": "3brTv10=","X-Ig-App-Id": "567067343352427","Priority": "u=3","User-Agent": f"Instagram 303.0.0.0.59 Android (28/9; 320dpi; 900x1600; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}/{''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; en_GB;)","Accept-Language": "ar-SA, en-US","Ig-Intended-User-Id": "0","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Content-Length": "1957","Accept-Encoding": "gzip, deflate","X-Fb-Http-Engine": "Liger","X-Fb-Client-Ip": "True","X-Fb-Server-Cluster": "True"}
    
    response = requests.post('https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.login.async.send_login_request/',headers=headers ,data=data)
    body = response.text
    
    if "Bearer" in body:
        session = re.search(r'Bearer IGT:2:(.*?),',response.text).group(1).strip()
        session = session[:-8]
        full=base64.b64decode(session).decode('utf-8')
        if "sessionid"  in full:
            sessionid = re.search(r'"sessionid":"(.*?)"}',full).group(1).strip()
            
            print(f"{green}[ + ] Logged in with @{user}{reset}")
            print(f"{cyan}[ + ] Session ID is :{reset}\n{yellow}{sessionid}{reset}")
            input(f"\n{blue}[ ! ] Press Enter to continue...{reset}")
            return sessionid
    elif "The password you entered is incorrect" in body or "Please check your username and try again." in body or "inactive user" in body or "should_dismiss_loading\", \"has_identification_error\"" in body:
        print(f"{red}[ - ] Bad Password{reset}")
        input()
        exit()
    elif "challenge_required" in body or "two_step_verification" in body:
        print(f"{yellow}[ ! ] Challenge required - accept and click enter{reset}")
        input()
        return extract_sessionid(user, password)
    else:
        print(f"{red}[ ! ] Something wrong{reset}")
        input()
        exit()

def starter():
    header()
    
    print(f"{cyan}[ ? ] Do you want to extract your Session ID? {yellow}(y/n){reset}: ", end='')
    choice = input().strip().lower()
    
    if choice == 'y' or choice == 'yes':
        print("\n" + "="*60)
        USER = str(input(f"{blue}[ + ] Username {reset}: "))
        PASSW = str(input(f"{blue}[ + ] Password {reset}: "))
        print("="*60 + "\n")
        
        sessionid = extract_sessionid(USER, PASSW)
        
        # طباعة فراغات للشكل
        print("\n" * 5)
        
        console.print("- Login Done [bold green]succ_Login[/bold green] ")
    else:
        sessionid = input(f"{blue}[+] SESSION ID :{reset} ").strip()
        
        if sessionid == "":
            console.print("[!] You must write The session ID")
            exit()
        
        console.print("- Verifying session...")
        
        is_valid, csrftoken_temp = verify_session(sessionid)
        
        if not is_valid:
            console.print("- [bold red]Invalid[/bold red] or [bold red]Expired[/bold red] Session ID!")
            exit()
        
        console.print("- Login Done [bold green]succ_Login[/bold green] ")
    
    # استخراج csrftoken
    is_valid, csrftoken = verify_session(sessionid)
    
    target = input("- Target username : ")
    
    r2 = post('https://i.instagram.com:443/api/v1/users/lookup/',
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
             data={"signed_body": "35a2d547d3b6ff400f713948cdffe0b789a903f86117eb6e2f3e573079b2f038.{\"q\":\"%s\"}" % target})
    
    if 'No users found' in r2.text:
        adv_search = get(f'https://www.instagram.com/{target}',
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
                        })
        try:
            target_id = re.findall('"profile_id":"(.*?)"', adv_search.text)[0]
            Report_Instagram(target_id, sessionid, csrftoken)
        except IndexError:
            try:
                target_id = re.findall('"page_id":"profilePage_(.*?)"', adv_search.text)[0]
                Report_Instagram(target_id, sessionid, csrftoken)
            except IndexError:
                try:
                    adv_search2 = get(f'https://www.instagram.com/api/v1/users/web_profile_info/?username={target}',
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
                                     })
                    target_id = adv_search2.json()['data']['user']['id']
                    Report_Instagram(target_id, sessionid, csrftoken)
                except KeyError:
                    console.print('\n- [bold red]Failed[/bold red] to get target username, Try entering the Target ID manually .\n')
                    target_id = input('- Enter The Target ID : ')
                    Report_Instagram(target_id, sessionid, csrftoken)
    elif '"spam":true' in r2.text:
        console.print("- Try again Later !")
        exit()
    else:
        try:
            target_id = str(r2.json()['user_id'])
            Report_Instagram(target_id, sessionid, csrftoken)
        except KeyError:
            console.print('- General [bold red]Error[/bold red] ...')
            exit()

header()
starter()
