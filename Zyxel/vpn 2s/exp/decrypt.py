import base64
import hashlib
import struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
# PKCS7 padding is typically handled by finalize() by default.
# from cryptography.hazmat.primitives import padding

def evp_bytestokey(password_bytes, salt_bytes, key_len, iv_len, md_alg_constructor, iterations):
    """
    Derives key and IV from password and salt, mimicking OpenSSL's EVP_BytesToKey.
    
    Args:
        password_bytes (bytes): The password.
        salt_bytes (bytes): The salt (should be 8 bytes for traditional PKCS5_SALT_LEN).
        key_len (int): Desired key length in bytes.
        iv_len (int): Desired IV length in bytes.
        md_alg_constructor: A hashlib digest algorithm constructor (e.g., hashlib.sha1).
        iterations (int): The 'count' parameter from EVP_BytesToKey.
                           It's the number of times the hash is applied iteratively.
    
    Returns:
        tuple: (key, iv) as bytes.
    """
    target_len = key_len + iv_len
    derived_bytes = b''
    prev_digest_block = b''  # Stores the D_{i-1} block

    while len(derived_bytes) < target_len:
        hasher = md_alg_constructor()
        if prev_digest_block:
            hasher.update(prev_digest_block)
        hasher.update(password_bytes)
        if salt_bytes: # Salt is only used if provided
            hasher.update(salt_bytes)
        
        # This is the first hash: MD(D_{i-1} || data || salt)
        current_digest_segment = hasher.digest()

        # Apply further iterations if count > 1
        # For MD^count(...), we need (iterations - 1) more hashes on current_digest_segment
        for _ in range(1, iterations):
            iter_hasher = md_alg_constructor()
            iter_hasher.update(current_digest_segment)
            current_digest_segment = iter_hasher.digest()
        
        derived_bytes += current_digest_segment
        prev_digest_block = current_digest_segment # This D_i becomes D_{i-1} for the next round

    return derived_bytes[:key_len], derived_bytes[key_len : key_len + iv_len]

def decrypt_key(b64_ciphertext_str):
    encrypt_key_str = "ThiSISEncryptioNKeY"
    # The 'passwd' variable from C ("N3z0y93") is not used in the decryption flow.
    
    # b64_ciphertext_str = "KBwy+/qk6a5E5c/NrR8BDg=="

    # Prepare salt
    # C code: int salt_arr[2]; salt_arr[0] = htonl(12345); salt_arr[1] = htonl(54321);
    # htonl ensures network byte order (big-endian).
    # An 'int' in C is typically 4 bytes.
    salt_val1 = 12345
    salt_val2 = 54321
    # ">I" packs as a big-endian unsigned int (4 bytes).
    salt_bytes = struct.pack(">I", salt_val1) + struct.pack(">I", salt_val2)
    # Expected salt: b'\x00\x00\x30\x39\x00\x00\xd4\x31'

    password_bytes = encrypt_key_str.encode('utf-8')

    # Parameters for key derivation from EVP_BytesToKey in C:
    # EVP_aes_256_cbc() -> AES-256, so 32-byte key. CBC mode IV is typically block size (16 bytes for AES).
    # EVP_sha1() -> SHA1 digest.
    # count = 5 -> 5 iterations.
    aes_key_len_bytes = 32
    aes_iv_len_bytes = 16 # AES block size is 128 bits (16 bytes)
    pbkdf_iterations = 5
    digest_algorithm = hashlib.sha1

    # Derive key and IV
    key, iv = evp_bytestokey(
        password_bytes,
        salt_bytes,
        aes_key_len_bytes,
        aes_iv_len_bytes,
        digest_algorithm,
        pbkdf_iterations
    )

    # For debugging (optional):
    # print(f"Derived Key (hex): {key.hex()}")
    # print(f"Derived IV (hex):  {iv.hex()}")

    # Base64 decode the ciphertext
    try:
        # The input string must be properly padded for standard Base64.
        # Python's b64decode can sometimes handle missing padding if the length is unambiguous.
        ciphertext_bytes = base64.b64decode(b64_ciphertext_str)
    except base64.binascii.Error as e:
        print(f"Error: Base64 decoding failed: {e}")
        print("Ensure the input is valid Base64 and correctly padded if necessary.")
        return
        
    print(f"base64 decode len:{len(ciphertext_bytes)}")

    # Perform AES Decryption (AES-256-CBC)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        # Decrypt the data. The finalize() method also handles unpadding (PKCS#7 by default).
        decrypted_bytes = decryptor.update(ciphertext_bytes) + decryptor.finalize()
        
        print(f"output len:{len(decrypted_bytes)}")
        
        # Try to decode as UTF-8 to print as a string.
        # If the decrypted data is not text, this might fail or produce garbled output.
        # The C code's printf("%s", out) has similar risks.
        try:
            decrypted_text = decrypted_bytes.decode('utf-8')
            print(f"{decrypted_text}")
        except UnicodeDecodeError:
            print("(Decrypted data is not valid UTF-8 text or contains null bytes)")
            # print(f"Decrypted data (raw bytes): {decrypted_bytes}")


        # Print integer value of each byte, similar to the C code's loop
        for byte_val in decrypted_bytes:
            print(byte_val, end="") # Prints integers from 0-255
        print("\n")

    except ValueError as e:
        # This error often occurs if the padding is incorrect, which can be a sign of:
        # - Incorrect key or IV (most common)
        # - Corrupted ciphertext
        # - Mismatch in encryption/decryption parameters (e.g., padding scheme)
        print(f"AES decryption error: {e}")
        print("This might be due to an incorrect key/IV, corrupted data, or padding issues.")
    
    return decrypted_text

if __name__ == "__main__":
    b64_ciphertext_str = "KBwy+/qk6a5E5c/NrR8BDg=="
    decrypt_key(b64_ciphertext_str)