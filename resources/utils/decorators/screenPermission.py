import flask
import functools
import datetime
from resources.db.executeSProc import fn_call_stored_procedure

def fn_check_screen_permission():
    """
    check user permission for screen
    will also add current screen id to request object
    """

    def decorator(function):
        @functools.wraps(function)
        def wrapper(request, *args, **kwargs):
            print("------------ start decorator check permission -------------", datetime.datetime.now())
            print("start time for check permission decorator", datetime.datetime.now())

            screen_id = int(flask.request.headers.get('screen_id'))
            user_id = int(flask.request.headers.get('user_id'))
            session_id = int(flask.request.headers.get('session_id'))
            student_entity_id = int(flask.request.headers.get('student_entity_id'))
            token = flask.request.headers.get('token')

            check_permission_output_params = [1, 1, 0, 0, 0]
            print("start time for check permission stored procedure", datetime.datetime.now())
            sproc_result_sets, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_sec_check_screen_permission_v2',
                                                                 screen_id,
                                                                 user_id,
                                                                 session_id,
                                                                 student_entity_id,
                                                                 token,
                                                                 *check_permission_output_params)
            
            print("end time for check permission stored procedure", datetime.datetime.now())
            
            # screen_permission_result_sets[5] == valid access & screen_permission_result_sets[7] == err_flag
            if (sproc_result_sets[5] == 0):
                return { 'Status': 'Failure', 'Message': sproc_result_sets[9]}, 400
            else:
                kwargs['screen_id'] = screen_id
                kwargs['user_id'] = user_id
                kwargs['session_id'] = session_id
                kwargs['token'] = token

                print("end time for check permission decorator", datetime.datetime.now())
                print("------------ end decorator check permission -------------", datetime.datetime.now())
                return function(request, *args, **kwargs)

        return wrapper

    return decorator

