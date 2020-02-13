from flask_restful import Resource
from flask import request

from resources.db.executeSProc import fn_call_stored_procedure, fn_sproc_response
from resources.utils.decorators.clientDBConnection import fn_make_client_db_connection
from resources.utils.decorators.screenPermission import fn_check_screen_permission


class clsLkpOrgAccount(Resource):

    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    def get(self, *args, **kwargs):
        try:
            debug_sproc = request.headers.get('debug_sproc')
            audit_screen_visit = request.headers.get('audit_screen_visit')

            account_lkp_output_params = [0, 0, 0]
            sproc_result_args, cursor = fn_call_stored_procedure(
                kwargs['client_db_connection'],
                'sproc_org_lkp_account',
                kwargs['session_id'],
                kwargs['user_id'],
                kwargs['screen_id'],
                debug_sproc,
                audit_screen_visit,
                *account_lkp_output_params)

            # sproc_result_args[5] = err_flag & sproc_result_args[7] = err_msg
            if sproc_result_args[5] == 1:
                return {'status': 'Failure', 'data': sproc_result_args[7]}, 200
            else:
                sproc_result_sets = fn_sproc_response(cursor)

                return {'status': 'Success', 'data': sproc_result_sets}, 200

        except Exception as e:
            return {'Error': str(e)}, 400

