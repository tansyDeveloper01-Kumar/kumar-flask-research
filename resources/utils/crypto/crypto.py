from cryptography.fernet import Fernet
import os

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
    return hash(key)