import mysql.connector
import os

from resources.db.executeSProc import fn_call_stored_procedure, fn_sproc_response


# connect to master db and get client db connection details
# static connection
def fn_sama_get_client_DB_details(user_domain_name):
    try:
        print("========= Calling fn_sama_get_client_DB_details ============")
        connection = fn_connect_client_db(host="35.221.182.51",
                                          database="sama_master",
                                          user="masterdbuser",
                                          password="xx9mastermysql6xx")

        print("================")
        print("fn_sama_get_client_DB_details", connection)
        print("================")
        connection_type = isinstance(connection, str)
        if connection_type == True:
            return connection, 400
        else:
            sproc_result_args, cursor = fn_call_stored_procedure(connection,
                                                                 'sproc_sama_get_client_db_connnection_info_v2',
                                                                 user_domain_name, 1, 1, 0, 0, 0)
            sproc_result_sets = fn_sproc_response(cursor)
            fn_close_db_connection(connection, cursor)
            print("================")
            print("sproc_sama_get_client_db_connnection_info_v2", sproc_result_sets)
            print("================")
            return sproc_result_sets, sproc_result_args
    except mysql.connector.Error as e:
        print("================")
        print("fn_sama_get_client_DB_details error", e)
        print("================")
        return str(e), 400


# connect to client db
# dynamic in nature, db name changed at run time based upon user login id/domain
def fn_connect_client_db(**kwargs):
    try:
        print("========= Calling fn_connect_client_db ============")
        connection = mysql.connector.connect(host=kwargs['host'],
                                             database=kwargs['database'],
                                             user=kwargs['user'],
                                             password=kwargs['password'])
        print("================")
        print("fn_connect_client_db", connection)
        print("================")
        return connection
    except mysql.connector.Error as error:
        print("================")
        print("fn_connect_client_db error", error)
        print("================")
        return str(error)


# close database connection
def fn_close_db_connection(connection, cursor):
    if connection.is_connected():
        connection.close()
        cursor.close()



