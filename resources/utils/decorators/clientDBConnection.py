import flask
import functools

from resources.db.dbConnect import fn_connect_client_db
from resources.utils.crypto.crypto import fn_decrypt
import datetime

def fn_make_client_db_connection():
    """
    check db connection
    """
    def decorator(function):
        @functools.wraps(function)
        def wrapper(request, *args, **kwargs):
            print("+++++++++++++++ start connection db decoarator call method +++++++++++++++", datetime.datetime.now())
            
            encrypt_db_user = flask.request.headers.get('encrypt_db_user')
            encrypt_db_pwd = flask.request.headers.get('encrypt_db_pwd')
            encrypt_db_host = flask.request.headers.get('encrypt_db_host')
            encrypt_db_database = flask.request.headers.get('encrypt_db_database')

            print("******  decrypt start time  ********", datetime.datetime.now())

            print("****  decrypt database start time ******", datetime.datetime.now())
            db_name = fn_decrypt(encrypt_db_database)
            print("****  decrypt database end time ******", datetime.datetime.now())
            print("****  decrypt user start time ******", datetime.datetime.now())
            db_user = fn_decrypt(encrypt_db_user)
            print("****  decrypt user end time ******", datetime.datetime.now())
            print("****  decrypt pwd start time ******", datetime.datetime.now())
            db_pwd = fn_decrypt(encrypt_db_pwd)
            print("****  decrypt pwd end time ******", datetime.datetime.now())
            print("****  decrypt host start time ******", datetime.datetime.now())
            db_host = fn_decrypt(encrypt_db_host)
            print("****  decrypt host end time ******", datetime.datetime.now())

            print("******  decrypt end time  ********", datetime.datetime.now())
                       
            print("******  start time for client db connect  ********", datetime.datetime.now())
            client_db_connection = fn_connect_client_db(user=db_user,
                                                        password=db_pwd,
                                                        database=db_name,
                                                        host=db_host)

            kwargs['client_db_connection'] = client_db_connection
            print("return time for client db connect", datetime.datetime.now())
            print("+++++++++++++++ end connection db decoarator call method +++++++++++++++", datetime.datetime.now())  
            return function(request, *args, **kwargs)

        return wrapper
    return decorator

