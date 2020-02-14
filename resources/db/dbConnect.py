import mysql.connector
import os

from resources.db.executeSProc import fn_call_stored_procedure, fn_sproc_response


# connect to master db and get client db connection details
# static connection
def fn_sama_get_client_DB_details(user_domain_name):
    try:
        connection = fn_connect_client_db(host=os.getenv("MH"),
                                         database=os.getenv("MDN"),
                                         user=os.getenv("MDU"),
                                         password=os.getenv("MDP"))

        connection_type = isinstance(connection, str)
        if connection_type == True:
            return connection, 400
        else:
            sproc_result_args, cursor = fn_call_stored_procedure(connection,
                                                                 'sproc_sama_get_client_db_connnection_info_v2',
                                                                 user_domain_name, 1, 1, 0, 0, 0)
            sproc_result_sets = fn_sproc_response(cursor)
            fn_close_db_connection(connection, cursor)
            return sproc_result_sets, sproc_result_args
    except mysql.connector.Error as e:
        return str(e)


# connect to client db
# dynamic in nature, db name changed at run time based upon user login id/domain
def fn_connect_client_db(**kwargs):
    try:
        connection = mysql.connector.connect(host=kwargs['host'],
                                             database=kwargs['database'],
                                             user=kwargs['user'],
                                             password=kwargs['password'])
        return connection
    except mysql.connector.Error as error:
        return str(error)


# close database connection
def fn_close_db_connection(connection, cursor):
    if connection.is_connected():
        connection.close()
        cursor.close()



