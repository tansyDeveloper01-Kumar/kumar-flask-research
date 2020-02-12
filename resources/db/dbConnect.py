import mysql.connector
from mysql.connector import Error
import os

from resources.db.executeSProc import fn_call_stored_procedure, fn_sproc_response


# connect to master db and get client db connection details
# static connection
def fn_get_client_DB_details(user_domain_name):
    connection = fn_connect_client_db(host=os.getenv("MH"),
                                     database=os.getenv("MDN"),
                                     user=os.getenv("MDU"),
                                     password=os.getenv("MDP"))

    result_args, cursor = fn_call_stored_procedure(connection,
                                                   'sproc_sama_get_client_db_connnection_info_v2',
                                                   user_domain_name, 1, 1, 0, 0, 0)

    sproc_result = fn_sproc_response(cursor)
    close_db_connection(connection, cursor)
    return sproc_result, result_args


# connect to client db
# dynamic in nature, db name changed at run time based upon user login id/domain
def fn_connect_client_db(**kwargs):
    try:
        connection = mysql.connector.connect(host=kwargs['host'],
                                             database=kwargs['database'],
                                             user=kwargs['user'],
                                             password=kwargs['password'])
        return connection
    except Error as error:
        return str(error)


# close database connection
def close_db_connection(connection, cursor):
    if connection.is_connected():
        connection.close()
        cursor.close()



