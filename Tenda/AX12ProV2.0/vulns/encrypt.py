from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# === 配置（与 JS 一致） ===
IV = "EU5H62G9ICGRNI43".encode("utf-8")
KEY = "V6hRnaxlxgcW6bQi".encode("utf-8")

# AES block size = 16 bytes
BLOCK_SIZE = 16


def encrypt(data: str) -> str:
    """模仿 JS 的 l.b.encrypt，AES-CBC + PKCS7，返回 Base64"""

    cipher = AES.new(KEY, AES.MODE_CBC, IV)

    # JS 中若为对象就 JSON.stringify，因此 Python 中由调用者决定提供字符串
    data_bytes = data.encode("utf-8")

    encrypted = cipher.encrypt(pad(data_bytes, BLOCK_SIZE))

    # JS 中是 Base64.stringify(ciphertext)
    return base64.b64encode(encrypted).decode("utf-8")


def decrypt(b64_ciphertext: str) -> str:
    """模仿 JS 的 l.b.decrypt，接收 Base64，加密模式同上"""

    cipher = AES.new(KEY, AES.MODE_CBC, IV)

    ciphertext = base64.b64decode(b64_ciphertext)

    decrypted = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)

    return decrypted.decode("utf-8")

if __name__ == "__main__":
    ciphertext = "ZHgz2ea2XcbvB6kUqt/QixMhMa0etTTDjkXO6+ZIOliWJXa4nbzu4JBopH51BQ3zI+tNiP38HOci76To5WWjyzgRZDc9dwrCH3Yo5GWkBp8i9OHrO6BOJ5biPyesv4o3rvdownMycz3Gz8F2NMVdJQP3yozlJpdX9CVdHt1LXFefe4L6SA6czcFvLtmit0tLuyuw+Hvrbsb2IHXLIyQ5iJ8bqm48Zcz8nQRM8zhsxmuvNgwZHMt9QwB7ozirTmI2"

    dec = decrypt(ciphertext)

    print(f"Decrypt Result: {dec}")
