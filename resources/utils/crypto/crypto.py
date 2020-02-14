import os
import hashlib
from cryptography.fernet import Fernet

def fn_encrypt(secret):
  x = os.getenv("MX")
  f = Fernet(x)

  secret_byte = secret.encode('utf-8')

  cipher = f.encrypt(secret_byte)

  return cipher

def fn_decrypt(cipher):
    x = os.getenv("MX")
    f = Fernet(x)

    cipher_byte = cipher.encode('utf-8')

    key = f.decrypt(cipher_byte).decode()

    return key

def fn_hash(key):
    try:
        m = hashlib.sha256()
        key_byte = key.encode('utf-8')
        m.update(key_byte)
        hash_sha256_key = m.hexdigest()
        return str(hash_sha256_key)
    except Exception as e:
        return str(e)
