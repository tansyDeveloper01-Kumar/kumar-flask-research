import mysql.connector
from mysql.connector import Error
import os


def connect_to_database(**kwargs):
    try:
        connection = mysql.connector.connect(host=kwargs['host'], database=kwargs['database'], user=kwargs['user'],
                                             password=kwargs['password'])
        return connection
    except Error as error:
        print("Failed to execute stored procedure: {0}".format(error))


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


def close_connection(connection, cursor):
    if connection.is_connected():
        connection.close()
        cursor.close()
        print('MySQL connection is closed')


def get_client_details_from_master_db(user_domain_name):
    connection = connect_to_database(host=os.getenv("MYSQL_HOST"), database=os.getenv("MASTER_DB_NAME"),
                                     user=os.getenv("MASTER_DB_USER"),
                                     password=os.getenv("MASTER_DB_PASSWORD"))
    result_args, cursor = call_stored_procedure(connection, 'sproc_sama_get_client_db_connnection_info_v2',
                                                user_domain_name, 1, 1, 0, 0, 0)
    print(result_args)
    sproc_result = sproc_response(cursor)
    close_connection(connection, cursor)
    return sproc_result


def is_token_valid(token):
    connection = connect_to_database(host=os.getenv("MYSQL_HOST"), database=os.getenv("MASTER_DB_NAME"),
                                     user=os.getenv("MASTER_DB_USER"),
                                     password=os.getenv("MASTER_DB_PASSWORD"))
    result_args, cursor = call_stored_procedure(connection, 'sproc_sama_validate_token', token, 0, 0, 9)
    print(result_args)
    sproc_result = sproc_response(cursor)
    close_connection(connection, cursor)
    return sproc_result, result_args
