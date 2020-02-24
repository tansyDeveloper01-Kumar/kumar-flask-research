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

    secret = f.decrypt(cipher_byte).decode()

    return secret

def fn_hash(secret):
    try:
        hash_method = hashlib.sha256()
        secret_byte = secret.encode('utf-8')
        hash_method.update(secret_byte)
        hash_sha256_key = hash_method.hexdigest()
        return str(hash_sha256_key)
    except Exception as e:
        return str(e)
