import flask
import functools
import os
from cryptography.fernet import Fernet

from resources.db.dbConnect import fn_connect_client_db
from resources.utils.crypto.crypto import fn_decrypt

def fn_make_client_db_connection():
    """
    check user permission for screen
    will also add current screen id to request object
    """
    def decorator(function):
        @functools.wraps(function)
        def wrapper(request, *args, **kwargs):

            encrypt_db_user = flask.request.headers.get('encrypt_db_user')
            encrypt_db_pwd = flask.request.headers.get('encrypt_db_pwd')
            encrypt_db_host = flask.request.headers.get('encrypt_db_host')
            encrypt_db_database = flask.request.headers.get('encrypt_db_database')

            db_name = fn_decrypt(encrypt_db_database)
            db_user = fn_decrypt(encrypt_db_user)
            db_pwd = fn_decrypt(encrypt_db_pwd)
            db_host = fn_decrypt(encrypt_db_host)
                       
            client_db_connection = fn_connect_client_db(user=db_user,
                                                        password=db_pwd,
                                                        database=db_name,
                                                        host=db_host)

            kwargs['client_db_connection'] = client_db_connection
            return function(request, *args, **kwargs)

        return wrapper
    return decorator

