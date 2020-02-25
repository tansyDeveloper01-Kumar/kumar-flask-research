import os
import hashlib
from cryptography.fernet import Fernet

def fn_encrypt(secret):
  x = "DBFFD8B07B1DECB98577F7ED1D78AA2E994111C03EC="
  print("+++++++++++++++ Calling fn_encrypt ++++++++++++++++++++++")
  print("++++++++++++++++")
  print("fn_encrypt", x)
  print("++++++++++++++++")
  f = Fernet(x)

  secret_byte = secret.encode('utf-8')

  cipher = f.encrypt(secret_byte)
  print("++++++++++++++++")
  print("fn_encrypt cipher", cipher)
  print("++++++++++++++++")

  return cipher

def fn_decrypt(cipher):
    x = "DBFFD8B07B1DECB98577F7ED1D78AA2E994111C03EC="
    print("+++++++++++++++ Calling fn_decrypt ++++++++++++++++++++++")
    f = Fernet(x)
    print("++++++++++++++++")
    print("fn_decrypt", x)
    print("++++++++++++++++")

    cipher_byte = cipher.encode('utf-8')

    secret = f.decrypt(cipher_byte).decode()

    print("++++++++++++++++")
    print("fn_decrypt", secret)
    print("++++++++++++++++")
    return secret

def fn_hash(secret):
    try:
        print("+++++++++++++++ Calling fn_hash ++++++++++++++++++++++")
        hash_method = hashlib.sha256()
        secret_byte = secret.encode('utf-8')
        hash_method.update(secret_byte)
        hash_sha256_key = hash_method.hexdigest()
        print("++++++++++++++++")
        print("fn_hash", str(hash_sha256_key))
        print("++++++++++++++++")
        return str(hash_sha256_key)
    except Exception as e:
        print("++++++++++++++++")
        print("fn_hash error", str(e))
        print("++++++++++++++++")
        return str(e)
