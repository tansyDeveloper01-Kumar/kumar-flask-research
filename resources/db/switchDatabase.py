import mysql.connector
from mysql.connector import Error

from resources.db.procedure import call_stored_procedure, sproc_response 


def get_client_details_from_master_db(user_domain_name):
    connection = connect_to_database(host="104.199.137.128", 
                                    database="sama_master",
                                    user="masterdbuser",
                                    password="xx9mastermysql6xx")

    result_args, cursor = call_stored_procedure(connection,'sproc_sama_get_client_db_connnection_info_v2', user_domain_name, 1, 1, 0, 0, 0)
    
    sproc_result = sproc_response(cursor)
    close_connection(connection, cursor)
    return sproc_result, result_args

def connect_to_database(**kwargs):
    try:
        connection = mysql.connector.connect(host=kwargs['host'], 
                                            database=kwargs['database'], 
                                            user=kwargs['user'],
                                            password=kwargs['password'])
        return connection
    except Error as error:
        return str(error)

def close_connection(connection, cursor):
    if connection.is_connected():
        connection.close()
        cursor.close()


