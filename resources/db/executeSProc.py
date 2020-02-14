import mysql.connector

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

