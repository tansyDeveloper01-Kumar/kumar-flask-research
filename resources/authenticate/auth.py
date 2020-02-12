from flask_restful import Resource
from flask import request

from resources.db.dbConnect import (fn_get_client_DB_details,
                                    fn_connect_client_db, close_db_connection)

from resources.db.executeSProc import fn_call_stored_procedure, fn_sproc_response
from resources.utils.crypto.crypto import fn_decrypt


class clsLogin(Resource):
    
    def get(self):
        try:
            data = request.get_json()
            user_id = data.get('domain_name')
            password = data.get('password')
            login_id, domain_name = user_id.split('@', 1)

            result_sets, result_args = fn_get_client_DB_details(user_domain_name=domain_name)

            if result_args[3] == 1:
                return {'status': 'Failure', 'data': result_args[5] }, 400
            else:
                client_db_details = result_sets[0]

                if client_db_details[0] is None:
                    return {'status': 'Failure', 'data': 'Invalid login' }, 400
                if not client_db_details:
                    return {'status': 'Failure', 'data': 'Client database not found'}, 400

                token = client_db_details[0]

                db_name = fn_decrypt(client_db_details[1])
                db_user = fn_decrypt(client_db_details[2])
                db_pwd = fn_decrypt(client_db_details[3])
                db_host = fn_decrypt(client_db_details[4])

                client_db_connection = fn_connect_client_db(user=db_user,
                                                            password=db_pwd,
                                                            database=db_name,
                                                            host=db_host)
                output_params = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                
                result_args, cursor = fn_call_stored_procedure(client_db_connection,
                                                            'sproc_sec_login_v2', 
                                                            login_id, 
                                                            password,
                                                            request.remote_addr, 
                                                            "desktop", 
                                                            token, *output_params)
                
                result_sets = fn_sproc_response(cursor)
                                
                if result_args[10] == "Success":                
                    result_sets_array = [result_set[0] for result_set in result_sets]

                    close_db_connection(client_db_connection, cursor)

                    result_json = {
                        'token': token,
                        'audit_screen_visit': result_args[5],
                        'debug_sproc': result_args[6],
                        'session_id': result_args[7],
                        'user_id': result_args[8],
                        'login_success': result_args[9],
                        'module_names': result_sets_array,
                        'user': client_db_details[2],
                        'password': client_db_details[3],
                        'database': client_db_details[1],
                        'host': client_db_details[4]
                    }
                    return { 'Status': result_args[10], 'data': result_json}, 200
                else:
                    return { 'Status': 'Failure', 'data': result_args[10]}, 400
        except Exception as error:
            return {"error_response": error}, 400
        

