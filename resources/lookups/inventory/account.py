from flask_restful import Resource
from flask import request

from mysql.connector import Error

from resources.db.switchDatabase import connect_to_database, is_token_valid

from resources.db.procedure import call_stored_procedure, sproc_response, \
                                   error_response

class LookupInvAccount(Resource):
    def get(self):
        try:
            token = request.headers.get('token')
            sproc_result_array, result_args = is_token_valid(token)
            client_db_details = [sproc_result for sproc_result in sproc_result_array[0]]
            
            client_db_connection = connect_to_database(user=client_db_details[2], 
                                                       password=client_db_details[3],
                                                       database=client_db_details[1],
                                                       host=client_db_details[4])
            
            result_args, cursor = call_stored_procedure(client_db_connection, 
                                                    'sproc_org_lkp_account',
                                                    request.headers.get('session_id'), 
                                                    request.headers.get('user_id'),
                                                    110001, 1, 1, 0, 0, 0)
            sproc_result = sproc_response(cursor)
            if not sproc_result:
                return error_response(code=404, type='Not Found', message='Unit of measure not found', fbtrace_id=None), 404
            dropdown_data = [{'brand_id': each_product[0], 'brand': each_product[1]} for each_product in sproc_result]
            
            return {'status': 'Success', 'measure': dropdown_data}, 200
            
        except Exception as e:
            return {'Error': str(e)}, 400
        
        
    def put(self):
        try:
            token = request.headers.get('token')
            entity_id = request.headers.get('entity_id')
            
            sproc_result_array, result_args = is_token_valid(token)
            client_db_details = [sproc_result for sproc_result in sproc_result_array[0]]
            
            client_db_connection = connect_to_database(user=client_db_details[2], 
                                                        password=client_db_details[3],
                                                        database=client_db_details[1],
                                                        host=client_db_details[4])

            
            try:
                # result_args, cursor = call_stored_procedure(client_db_connection, 
                #                                     'sproc_inv_product_dml_del',
                #                                     request.headers.get('entity_id'),
                #                                     request.headers.get('session_id'), 
                #                                     request.headers.get('user_id'),
                #                                     110001, 1, 1, 0, 0, 0)
                # sproc_result = sproc_response(cursor)

                conn = client_db_connection.cursor()
                conn.callproc('sproc_inv_product_dml_del', (entity_id, 254, 20, 110001, 1, 1, 0, 0, 0))
                sproc_result = sproc_response(conn)
                print("===========")
                print(sproc_result)
                print("===========")
                if not sproc_result:
                    return error_response(code=404, type='Not Found', 
                                        message='product not found', 
                                        fbtrace_id=None), 404

                dropdown_data = [{'entity_id': each_product[0], 'deleted_flag': each_product[6]} for each_product in sproc_result]
                
                return {'status': 'Success', 'result': dropdown_data}, 200
            except Exception as e:
                return {'status': 'Success', "error": str(e)}, 200
                        
        except Exception as e:
            print("********", e, "********")
            return {'Error': str(e)}, 400
