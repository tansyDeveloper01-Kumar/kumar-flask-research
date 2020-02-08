from flask_restful import Resource
from flask import request

from resources.db.switchDatabase import connect_to_database, is_token_valid

from resources.db.procedure import call_stored_procedure, sproc_response, \
                                   error_response

class LookupInvUnitOfMeasure(Resource):
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
                                                    'sproc_inv_lkp_unit_of_measure',
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
        
