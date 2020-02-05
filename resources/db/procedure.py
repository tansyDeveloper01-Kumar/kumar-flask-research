import mysql.connector
from mysql.connector import Error

def call_stored_procedure(connection, sproc_name, *args):
    try:
        cursor = connection.cursor()
        result_args = cursor.callproc(sproc_name, args)
        return result_args, cursor
    except Error as error:
        print('Failed to execute stored procedure: {0}'.format(error))


def sproc_response(cursor):
    for result in cursor.stored_results():
        return result.fetchall()