import flask
import functools
import json
import os
from cryptography.fernet import Fernet

from resources.db.switchDatabase import connect_to_database, is_token_valid

def check_client_db_connection():
    """
    check user permission for screen
    will also add current screen id to request object
    """
    def decorator(function):
        @functools.wraps(function)
        def wrapper(request, *args, **kwargs):
            x = os.getenv("MX")
            f = Fernet(x)

            encrypt_db_user = flask.request.headers.get('encrypt_db_user').encode('utf-8')
            encrypt_db_pwd = flask.request.headers.get('encrypt_db_pwd').encode('utf-8')
            encrypt_db_host = flask.request.headers.get('encrypt_db_host').encode('utf-8')
            encrypt_db_database = flask.request.headers.get('encrypt_db_database').encode('utf-8')

            decode_db_user = f.decrypt(encrypt_db_user).decode()
            decode_db_pwd = f.decrypt(encrypt_db_pwd).decode()
            decode_db_host = f.decrypt(encrypt_db_host).decode()
            decode_database = f.decrypt(encrypt_db_database).decode()
                       
            client_db_connection = connect_to_database(user=decode_db_user,
                                                        password=decode_db_pwd,
                                                        database=decode_database,
                                                        host=decode_db_host)

            kwargs['client_db_connection'] = client_db_connection
            return function(request, *args, **kwargs)

        return wrapper
    return decorator

