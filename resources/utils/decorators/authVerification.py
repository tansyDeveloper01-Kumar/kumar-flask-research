import flask
import functools
import json

from resources.db.dbConnect import connect_to_database, is_token_valid

def check_auth_verification():
    """
    check user permission for screen
    will also add current screen id to request object
    """
    def decorator(function):
        @functools.wraps(function)
        def wrapper(request, *args, **kwargs):
            session_id = flask.request.headers.get('session_id')
            user_id = flask.request.headers.get('user_id')
            token = flask.request.headers.get('token')

            sproc_result_array, result_args = is_token_valid(token)

            if result_args[3] == "token expired":
                return {'status': "Failure", "Message": result_args[3]}
            elif result_args[3] == "invalid token":
                return {'status': "Failure", "Message": result_args[3]}
            else:
                if result_args[0] != token:
                    return {'status': "Failure", "Message": "Entered wrong token"}
                else:
                    client_db_connection = connect_to_database(user=sproc_result_array[0][2],
                                                               password=sproc_result_array[0][3],
                                                               database=sproc_result_array[0][1],
                                                               host=sproc_result_array[0][4])
                    kwargs['client_db_connection'] = client_db_connection
                    return function(request, *args, **kwargs)

        return wrapper
    return decorator

