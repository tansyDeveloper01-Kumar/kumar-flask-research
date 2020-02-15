import mysql.connector
import json
import datetime

# execute stored procedure
def fn_call_stored_procedure(connection, sproc_name, *args):
    try:
        cursor = connection.cursor()
        sproc_result_args = cursor.callproc(sproc_name, args)
        return sproc_result_args, cursor
    except mysql.connector.Error as error:
        print('Failed to execute stored procedure: {0}'.format(error))
        return str(error), 400

# capture result sets from the stored procedure execution
def fn_sproc_response(cursor):
    for result in cursor.stored_results():
        return result.fetchall()

# return function
def fn_return_sproc_status(sproc_result_args, cursor, screen, functionality):
    sproc_result_args_type = isinstance(sproc_result_args, str)
    if sproc_result_args_type == True and cursor == 400:
        return {'status': 'Failure', 'data': sproc_result_args}, 400
    # sproc_result_args[5] = err_flag & sproc_result_args[7] = err_msg
    elif sproc_result_args[-3] == 1:
        return {'status': 'Failure', 'data': sproc_result_args[-1]}, 200
    else:
        sproc_result_sets = fn_sproc_response(cursor)

        return {'status': 'Success', 'data': sproc_result_sets, 'message': screen+functionality+"Successfully"}, 200

def fn_return_sproc_datefield_status(sproc_result_args, cursor, screen, functionality):
    sproc_result_args_type = isinstance(sproc_result_args, str)
    if sproc_result_args_type == True and cursor == 400:
        return {'status': 'Failure', 'data': sproc_result_args}, 400
    # sproc_result_args[5] = err_flag & sproc_result_args[7] = err_msg
    elif sproc_result_args[-3] == 1:
        return {'status': 'Failure', 'data': sproc_result_args[-1]}, 200
    else:
        sproc_result_sets = fn_sproc_response(cursor)
        res = json.dumps(sproc_result_sets, default=fn_date_converter)
        return {'status': 'Success', 'data': res, 'message': screen+functionality+"Successfully"}, 200


def fn_date_converter(data):
    if isinstance(data, datetime.datetime):
        return data.__str__()

