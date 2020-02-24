from flask_restful import Resource
from flask import request

from resources.db.dbConnect import (fn_sama_get_client_DB_details,
                                    fn_connect_client_db, fn_close_db_connection)

from resources.db.executeSProc import fn_call_stored_procedure, fn_sproc_response
from resources.utils.crypto.crypto import fn_decrypt, fn_hash


class clsLogin(Resource):
    
    def get(self):
        try:
            data = request.get_json()
            user_id = data.get('domain_name')
            password = data.get('password')
            hash_password = fn_hash(data.get('password'))

            login_id, domain_name = user_id.split('@', 1)

            sproc_sama_result_sets, sproc_sama_result_args = fn_sama_get_client_DB_details(user_domain_name=domain_name)

            if sproc_sama_result_args == 400:
                return {'status': 'Failure', 'data': sproc_sama_result_sets}, 400
            elif sproc_sama_result_args[-3] == 1:
                return {'status': 'Failure', 'data': sproc_sama_result_args[-1] }, 400
            else:
                client_db_details = sproc_sama_result_sets[0]

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
                sproc_result_args, cursor = fn_call_stored_procedure(client_db_connection,
                                                            'sproc_sec_login_v2', 
                                                            login_id, 
                                                            password,
                                                            request.remote_addr, 
                                                            "desktop", 
                                                            token, *output_params)
                
                sproc_result_sets = fn_sproc_response(cursor)

                if sproc_result_args[-4] == "Success":
                    get_module_names = [result_set[0] for result_set in sproc_result_sets]

                    fn_close_db_connection(client_db_connection, cursor)

                    result_json = {
                        'token': token,
                        'audit_screen_visit': sproc_result_args[5],
                        'debug_sproc': sproc_result_args[6],
                        'session_id': sproc_result_args[7],
                        'user_id': sproc_result_args[8],
                        'login_success': sproc_result_args[9],
                        'module_names': get_module_names,
                        'user': client_db_details[2],
                        'password': client_db_details[3],
                        'database': client_db_details[1],
                        'host': client_db_details[4]
                    }
                    return { 'Status': sproc_result_args[-4], 'data': "ok"}, 200
                else:
                    return { 'Status': 'Failure', 'data': sproc_result_args[-4], 'error': sproc_result_args[-1]}, 400
        except Exception as error:
            return {"error_response": error}, 400
        

