import flask
import functools

from resources.db.switchDatabase import connect_to_database, is_token_valid

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
                    return function(request, *args, **kwargs)

        return wrapper
    return decorator

