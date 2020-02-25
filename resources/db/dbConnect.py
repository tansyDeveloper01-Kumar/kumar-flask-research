import mysql.connector
import os

from resources.db.executeSProc import fn_call_stored_procedure, fn_sproc_response
import datetime

# connect to master db and get client db connection details
# static connection
def fn_sama_get_client_DB_details(user_domain_name):
    try:        
        connection = fn_connect_client_db(host="35.221.182.51",
                                          database="sama_master",
                                          user="masterdbuser",
                                          password="xx9mastermysql6xx")
        
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
        return str(e), 400


# connect to client db
# dynamic in nature, db name changed at run time based upon user login id/domain
def fn_connect_client_db(**kwargs):
    try:
        print("+++++++++++++++ client db +++++++++++++++")
        print("within function start time for client db connect", datetime.datetime.now())
        connection = mysql.connector.connect(host=kwargs['host'],
                                             database=kwargs['database'],
                                             user=kwargs['user'],
                                             password=kwargs['password'])
        
        print("within function return time for client db connect", datetime.datetime.now())
        print("+++++++++++++++ client db +++++++++++++++")
        return connection
    except mysql.connector.Error as error:
        return str(error)


# close database connection
def fn_close_db_connection(connection, cursor):
    if connection.is_connected():
        connection.close()
        cursor.close()
        print("end time for client db connect", datetime.datetime.now())
        print("+++++++++++++++ client db +++++++++++++++")



