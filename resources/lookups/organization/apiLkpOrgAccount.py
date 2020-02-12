from flask_restful import Resource
from flask import request

from resources.db.dbConnect import connect_to_database, is_token_valid

from resources.db.executeSProc import call_stored_procedure, sproc_response, \
                                   error_response

from resources.utils.decorators.check_client_db_connection import check_client_db_connection

class clsLkpOrgAccount(Resource):

    @check_client_db_connection()
    def get(self, *args, **kwargs):
        try:
            screen_id = request.headers.get('screen_id')
            user_id = request.headers.get('user_id')
            session_id = request.headers.get('session_id')
            student_entity_id = request.headers.get('student_entity_id')
            token = request.headers.get('token')

            result_arg, cursor1 = call_stored_procedure(kwargs['client_db_connection'],
                                                    'sproc_sec_check_screen_permission_v2',
                                                    screen_id, 
                                                    user_id,
                                                    session_id,
                                                    student_entity_id,
                                                    token, 1, 1, 0, 0, 0)

            if (result_arg[5] == 0 and result_arg[7] == 1):
                return { 'Status': 'Failure', 'Message': result_arg[9]}, 400
            else:
                result_args, cursor = call_stored_procedure(kwargs['client_db_connection'],
                                                        'sproc_org_lkp_account',
                                                        request.headers.get('session_id'), 
                                                        request.headers.get('user_id'),
                                                        110001, 1, 1, 0, 0, 0)
                sproc_result = sproc_response(cursor)
                
                dropdown_data = [{'brand_id': each_product[0], 'brand': each_product[1]} for each_product in sproc_result]
                
                return {'status': 'Success', 'measure': dropdown_data}, 200
            
        except Exception as e:
            return {'Error': str(e)}, 400
        
