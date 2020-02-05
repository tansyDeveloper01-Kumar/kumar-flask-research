from flask_restful import Resource
from flask import request

from resources.db.switchDatabase import (get_client_details_from_master_db,
                                        connect_to_database, close_connection)

from resources.db.procedure import call_stored_procedure, sproc_response                                      


class AuthBackend(Resource):
    
    def get(self):
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            password = data.get('password')
            login_id, domain_name = user_id.split('@', 1)
            client_db_details, result_args = get_client_details_from_master_db(user_domain_name=domain_name)
            
            client_db_details = client_db_details[0]
            if client_db_details[0] is None:
                return error_response(code=404, type='Not found', message='Invalid login', fbtrace_id=None), 404
            if not client_db_details:
                return error_response(code=404, type='Not Found', message='Client database not found', fbtrace_id=None), 404
            token = client_db_details[0]
            client_db_connection = connect_to_database(user=client_db_details[2], 
                                                    password=client_db_details[3],
                                                    database=client_db_details[1],
                                                    host=client_db_details[4])
            output_params = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            
            result_args, cursor = call_stored_procedure(client_db_connection, 'sproc_sec_login_v2', login_id, password,
                                                        request.remote_addr, "desktop", *output_params)
            required_output_params = result_args[4:8]
            error_params = result_args[-5:]
            result_sets = sproc_response(cursor)
            
            if 0 in error_params:
                return error_response(code=406, type='Not Acceptable', message='Server timed out', fbtrace_id=None), 406
            if result_sets is None:
                return error_response(code=406, type='Not Acceptable', message='Password is incorrect',
                                    fbtrace_id=None), 406
            
            result_sets_array = [result_set[0] for result_set in result_sets]
            
            close_connection(client_db_connection, cursor)
            result_json = {
                'token': token,
                'audit_screen_visit': required_output_params[0],
                'debug_sproc': required_output_params[1],
                'session_id': required_output_params[2],
                'user_id': required_output_params[3],
                'module_names': result_sets_array
            }
            return result_json
        except Exception as error:
            return {"error_response": error}, 400
        

