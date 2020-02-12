from flask import request
from flask_restful import Resource
from cryptography.fernet import Fernet
import os

class clsSysEncrypt(Resource):

    def get(self):
        x = os.getenv("MX")
        f = Fernet(x)

        data = request.get_json()

        db_user = data.get('db_user').encode('utf-8')
        db_pwd = data.get('db_pwd').encode('utf-8')
        db_host = data.get('db_host').encode('utf-8')
        db_database = data.get('db_database').encode('utf-8')

        result_json = {
                        'encrypt_db_user': str(f.encrypt(db_user)),
                        'encrypt_db_pwd': str(f.encrypt(db_pwd)),
                        'encrypt_db_host': str(f.encrypt(db_host)),
                        'encrypt_db_database': str(f.encrypt(db_database))
                      }

        return { 'data': result_json }, 200

class clsSysDecrypt(Resource):

    def get(self):
        x = os.getenv("MX")
        f = Fernet(x)

        data = request.get_json()

        encrypt_db_user = data.get('encrypt_db_user').encode('utf-8')
        encrypt_db_pwd = data.get('encrypt_db_pwd').encode('utf-8')
        encrypt_db_host = data.get('encrypt_db_host').encode('utf-8')
        encrypt_db_database = data.get('encrypt_db_database').encode('utf-8')

        result_json = {
                        'encrypt_db_user': f.decrypt(encrypt_db_user).decode(),
                        'encrypt_db_pwd': f.decrypt(encrypt_db_pwd).decode(),
                        'encrypt_db_host': f.decrypt(encrypt_db_host).decode(),
                        'encrypt_db_database': f.decrypt(encrypt_db_database).decode()
                      }

        return {'data': str(result_json) }, 200