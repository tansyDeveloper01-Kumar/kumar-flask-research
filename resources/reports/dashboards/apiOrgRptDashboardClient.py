from flask_restful import Resource
from flask import request

from resources.db.executeSProc import fn_call_stored_procedure, fn_sproc_response
from resources.utils.decorators.clientDBConnection import fn_make_client_db_connection
from resources.utils.decorators.screenPermission import fn_check_screen_permission

class clsOrgClientDashboard(Resource):

    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    # get multiple result sets used to populate client dashboard
    def get(self, *args, **kwargs):
        try:
            data = request.get_json()

            start_date = data.get('start_date')
            end_date = data.get('end_date')
            client_entity_id = int(data.get('client_entity_id'))

            debug_sproc = request.headers.get('debug_sproc')
            audit_screen_visit = request.headers.get('audit_screen_visit')

            input_params = [start_date, end_date, client_entity_id, kwargs['session_id'],kwargs['user_id'],
                       kwargs['screen_id'], debug_sproc, audit_screen_visit]

            output_params = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_org_rpt_dashboard_client',
                                                                 *input_params, *output_params)

            sproc_result_args_type = isinstance(sproc_result_args, str)
            if sproc_result_args_type == True and cursor == 400:
                return {'status': 'Failure', 'data': sproc_result_args}, 400
            # sproc_result_args[5] = err_flag & sproc_result_args[7] = err_msg
            elif sproc_result_args[5] == 1:
                return {'status': 'Failure', 'data': sproc_result_args[7]}, 200
            else:
                sproc_result = []
                for result in cursor.stored_results():
                    sproc_result.append(result.fetchall())
                        
            return {'status': 'Success', 'data': sproc_result}, 200
            
        except Exception as e:
            return {'Error': str(e)}, 400
