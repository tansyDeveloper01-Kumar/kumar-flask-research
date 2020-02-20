from flask_restful import Resource
from flask import request

from resources.db.executeSProc import fn_call_stored_procedure, fn_return_sproc_single_result_sets
from resources.utils.decorators.clientDBConnection import fn_make_client_db_connection
from resources.utils.decorators.screenPermission import fn_check_screen_permission


class clsInvLkpManufacture(Resource):

    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    def get(self, *args, **kwargs):
        try:
            debug_sproc = int(request.headers.get('debug_sproc'))
            audit_screen_visit = int(request.headers.get('audit_screen_visit'))

            input_params = [kwargs['session_id'], kwargs['user_id'], kwargs['screen_id'], debug_sproc,
                            audit_screen_visit]
            output_params = [0, 0, 0]
            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_inv_lkp_manufacture',
                                                                 *input_params,
                                                                 *output_params)

            return fn_return_sproc_single_result_sets(sproc_result_args=sproc_result_args, cursor=cursor,
                                                      functionality="Manufacture data fetched successfully")

        except Exception as e:
            return {'Error': str(e)}, 400

