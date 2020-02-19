import mysql.connector
import json

from resources.utils.serialize import clsCustomJSONEncoder

# execute stored procedure
def fn_call_stored_procedure(connection, sproc_name, *args):
    try:
        cursor = connection.cursor()
        sproc_result_args = cursor.callproc(sproc_name, args)
        return sproc_result_args, cursor
    except mysql.connector.Error as error:
        print('Failed to execute stored procedure: {0}'.format(error))
        return str(error), 400

# capture single result set from the stored procedure execution
def fn_sproc_response(cursor):
    for result in cursor.stored_results():
        return result.fetchall()

# capture multiple single result set from the stored procedure execution
def fn_sproc_multiple_result_sets_response(cursor):
    multiple_result = []
    for result in cursor.stored_results():
        multiple_result.append(result.fetchall())
    return multiple_result

def fn_get_sproc_errors(**kwargs):
    sproc_result_args_type = isinstance(kwargs['sproc_result_args'], str)
    if sproc_result_args_type == True and kwargs['cursor'] == 400:
        return 'Failure', kwargs['sproc_result_sets'], 400
    elif kwargs['sproc_result_args'][-3] == 1:
        return 'Failure', kwargs['sproc_result_args'][-1], 400
    else:
        return 'Success', kwargs['cursor'], 200

def fn_response_data(**kwargs):
    serialize_result = json.dumps(kwargs['sproc_result_sets'], cls=clsCustomJSONEncoder)
    deserialize_result = json.loads(serialize_result)
    return {'status': 'Success',
            'data': deserialize_result,
            'message': kwargs['screen'] + kwargs['functionality'] + "Successfully"}, kwargs['status_code']

# return function
def fn_return_sproc_status(sproc_result_args, cursor, screen, functionality):
    status, cursor_object, status_code = fn_get_sproc_errors(sproc_result_args, cursor)
    print(status, cursor_object, status_code)
    return "hello"

def fn_return_sproc_single_result_sets(**kwargs):
    status, cursor_object, status_code = fn_get_sproc_errors(**kwargs)
    if status == "Failure" and status_code == 400:
        return { 'status': status, 'data': cursor_object }, status_code
    else:
        sproc_single_result_set = fn_sproc_response(cursor_object)
        return fn_response_data(sproc_result_sets=sproc_single_result_set, screen=kwargs['screen'],
                                functionality=kwargs['functionality'], status_code=status_code)


def fn_return_sproc_multiple_result_sets(**kwargs):
    status, cursor_object, status_code = fn_get_sproc_errors(**kwargs)
    if status == "Failure" and status_code == 400:
        return { 'status': status, 'data': cursor_object }, status_code
    else:
        sproc_multiple_result_sets = fn_sproc_multiple_result_sets_response(cursor_object)
        return fn_response_data(sproc_result_sets = sproc_multiple_result_sets, screen = kwargs['screen'],
                                functionality = kwargs['functionality'], status_code = status_code)



