from flask_restful import Resource
from flask import request

from resources.db.executeSProc import fn_call_stored_procedure, fn_sproc_response
from resources.utils.decorators.check_client_db_connection import make_client_db_connection

class clsLkpOrgAccount(Resource):

    @make_client_db_connection()
    def get(self, *args, **kwargs):
        try:
            screen_id = request.headers.get('screen_id')
            user_id = request.headers.get('user_id')
            session_id = request.headers.get('session_id')
            debug_sproc = request.headers.get('debug_sproc')
            audit_screen_visit = request.headers.get('audit_screen_visit')
            student_entity_id = request.headers.get('student_entity_id')
            token = request.headers.get('token')

            check_permission_output_params = [1, 1, 0, 0, 0]
            screen_permission_result_sets, screen_permission_cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                    'sproc_sec_check_screen_permission_v2',
                                                    screen_id, 
                                                    user_id,
                                                    session_id,
                                                    student_entity_id,
                                                    token,
                                                    *check_permission_output_params)

            # screen_permission_result_sets[5] == valid access & screen_permission_result_sets[7] == error flag
            if (screen_permission_result_sets[5] == 0 and screen_permission_result_sets[7] == 1):
                return { 'Status': 'Failure', 'Message': screen_permission_result_sets[9]}, 400
            else:
                account_lkp_output_params = [0, 0, 0]
                account_lkp_result_args, account_lkp_cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                               'sproc_org_lkp_account',
                                                               session_id,
                                                               user_id,
                                                               screen_id,
                                                               debug_sproc,
                                                               audit_screen_visit,
                                                               *account_lkp_output_params)
                
                sproc_result = fn_sproc_response(account_lkp_cursor)

                account_data = [{
                                 'entity_id': each_account[0],
                                 'entity_name': each_account[1]
                                } for each_account in sproc_result
                               ]
                
                return {'status': 'Success', 'measure': account_data}, 200
            
        except Exception as e:
            return {'Error': str(e)}, 400
        
