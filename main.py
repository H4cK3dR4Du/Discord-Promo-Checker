import os

libraries_to_import = [
    "colorama",
    "requests",
    "tls_client",
    "pystyle",
    "datetime",
    "httpx"
]

for lib in libraries_to_import:
    try:
        exec(f"import {lib}")
    except ModuleNotFoundError:
        os.system(f"pip install {lib}")

import json, time, httpx, sys, threading, ctypes, random, string, concurrent.futures, requests
from colorama import Fore, init, Style
from pystyle import Write, System, Colors, Colorate
from threading import Lock , Thread , Timer
from datetime import datetime
from os.path import isfile, join
from tls_client import Session

output_lock = threading.Lock()
red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT

def get_time_rn():
    date = datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

total = 0
valid = 0
invalid = 0
redeemed = 0

ctypes.windll.kernel32.SetConsoleTitleW(f'[ Discord Promo Checker ] By H4cK3dR4Du#1337 ~ discord.gg/radutool')
def update_title():
    global total, valid, invalid, redeemed
    ctypes.windll.kernel32.SetConsoleTitleW(f'[ Discord Promo Checker ] | Valid : {valid} | Invalid : {invalid} | Redeemed : {redeemed} | Working Rate : {round(valid/total*100,2)}% | github.com/H4cK3dR4Du')

with open("proxies.txt", "a") as f:
    f.write("")

def save_proxies(proxies):
    with open("proxies.txt", "w") as file:
        file.write("\n".join(proxies))

def get_proxies():
    with open('proxies.txt', 'r', encoding='utf-8') as f:
        proxies = f.read().splitlines()
    if not proxies:
        proxy_log = {}
    else:
        proxy = random.choice(proxies)
        proxy_log = {
            "http://": f"http://{proxy}", "https://": f"http://{proxy}"
        }
    try:
        url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
        response = httpx.get(url, proxies=proxy_log, timeout=60)

        if response.status_code == 200:
            proxies = response.text.splitlines()
            save_proxies(proxies)
        else:
            time.sleep(1)
            get_proxies()
    except httpx.ProxyError:
        get_proxies()
    except httpx.ReadError:
        get_proxies()
    except httpx.ConnectTimeout:
        get_proxies()
    except httpx.ReadTimeout:
        get_proxies()
    except httpx.ConnectError:
        get_proxies()
    except httpx.ProtocolError:
        get_proxies()

def check_proxies_file():
    file_path = "proxies.txt"
    if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
        get_proxies()

check_proxies_file()

def check_promo(promo):
    global valid, invalid, total, redeemed

    session = Session(
            client_identifier="chrome_112",
            random_tls_extension_order=True
    )

    proxy = random.choice(open("proxies.txt", "r").readlines()).strip() if len(open("proxies.txt", "r").readlines()) != 0 else None
    if ":" in proxy and len(proxy.split(":")) == 4:
        ip, port, user, pw = proxy.split(":")
        proxy_string = f"http://{user}:{pw}@{ip}:{port}"
    else:
        ip, port = proxy.split(":")
        proxy_string = f"http://{ip}:{port}"

    session.proxies = {
        "http": proxy_string,
        "https": proxy_string
    }

    try:
        r = session.get(f"https://discord.com/api/v9/entitlements/gift-codes/{promo}?country_code=ES&with_application=false&with_subscription_plan=true")
        if "You are being rate limited." in r.text:
            check_promo(promo)
        elif r.status_code != 200 or "Unknown Gift Code" in r.text:
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Invalid {gray}|{pink} https://promos.discord.gg/{reset}{promo}")
            invalid += 1
            total += 1
            update_title()
        else:
            r_json = r.json()
            check_redeemed = r_json['redeemed']
            if check_redeemed == False:
                max_uses, uses = r_json['max_uses'], r_json['uses']
                if max_uses != uses:
                    promotion = r_json['promotion']['inbound_header_text'].split('T')[0]
                    expiry = str(promotion)
                    time_rn = get_time_rn()
                    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Valid {gray}|{pink} https://promos.discord.gg/{reset}{promo}")
                    valid += 1
                    total += 1
                    update_title()
                    with open("Results/valid_promo.txt", "a+", encoding='utf-8') as f:
                        f.write(f"Valid Promo ---> https://promos.discord.gg/{promo}")
                else:
                    time_rn = get_time_rn()
                    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({yellow}/{gray}) {pretty}Redeemed {gray}|{pink} https://promos.discord.gg/{reset}{promo}")
                    redeemed += 1
                    total += 1
                    update_title()        
    except:
        check_promo(promo)

try:
    with open("promos.txt", "r") as f:
        lines = f.readlines()
        promos = []
        for line in lines:
            index = line.find(".gg/")
            if index != -1:
                promo = line[index + 4:].strip()
                promos.append(promo)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(check_promo, promos)

except FileNotFoundError:
    pass
except Exception as e:
    raise

input()