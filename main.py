import re
import time
import string
import random
import requests
import subprocess
from json import dumps
from pygments import highlight, lexers, formatters

url = "https://www.instagram.com/accounts/emailsignup/"

response = requests.get(
    url = "https://www.instagram.com/accounts/emailsignup/",
    headers = {
        "host": "www.instagram.com",
        "connection": "keep-alive",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "referer": "https://www.google.com/",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"
    }
)

def __to_base36(n: int) -> str:
    chars = string.digits + string.ascii_letters

    if n == 0:
        return "0"
    
    result = ""
    while n:
        n, r = divmod(n, 36)
        result = chars[r] + result

    return result

def __q() -> str:
    a = random.randint(0, 36**6 - 1)
    a = __to_base36(a)

    return a.zfill(6)

def get_web_session_id() -> str:
    return __q() + ":" + __q() + ":" + __q()

def get_mid() -> str:
    h = [0, 0, 0, 0, 0, 0, 0, 0]
    h_str = ""

    for _ in h:
        rnd = random.randint(0, 4294967295)
        h_str += __to_base36(rnd)

    return h_str

def get_asbd_id() -> str:
    links = re.findall(r'<link rel="preload" href="(.*?)" as="script" crossorigin="anonymous"', response.text)

    for link in links:
        link_response = requests.get(link)

        if "ASBD_ID" in link_response.text:
            match = re.findall(r'a="(.*?)";f.ASBD_ID=a', link_response.text)[0]

            return match

    return "359341 #"

formatted_json = dumps({
    "X-ASBD-ID": get_asbd_id(),
	"X-CSRFToken": re.findall(r'"csrf_token":"(.*?)"', response.text)[0],
	"X-IG-App-ID": int(re.findall(r'"app_id":"(.*?)"', response.text)[0]),
	"X-IG-WWW-Claim": "0",
	"X-Instagram-AJAX": re.findall(r'data-btmanifest="(.*?)_main"', response.text)[0],
	"X-Mid": get_mid(),
	"X-Requested-With": "XMLHttpRequest",
	"X-Web-Device-Id": re.findall(r'"_js_ig_did":{"value":"([a-zA-Z0-9\-]+)"', response.text)[0],
	"X-Web-Session-ID": get_web_session_id(),
    "Cookie": {
        "datr": re.findall(r'"_js_datr":{"value":"([a-zA-Z0-9\-]+)"', response.text)[0],
        "ig_did": re.findall(r'"_js_ig_did":{"value":"([a-zA-Z0-9\-]+)"', response.text)[0],
        "mid": re.findall(r'"_js_mid":{"value":"([a-zA-Z0-9\-]+)"', response.text)[0],
        "csrftoken": re.findall(r'"csrf_token":"(.*?)"', response.text)[0]
    },
    "Blank-Password": "Juz0.@!#",
    "Encrypted-Password": subprocess.check_output([
        "node", "c.js", "237", "91b03050a79fb0148debef99bcd76494707018c3005a90d1a4eab63e1f38bc20", "Juz0.@!#", str(int(time.time()))
    ]).decode().strip()
}, indent = 4)

print(highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter()))