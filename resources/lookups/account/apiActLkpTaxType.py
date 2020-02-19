from flask_restful import Resource
from flask import request

from resources.db.executeSProc import fn_call_stored_procedure, fn_sproc_response, fn_get_sproc_errors
from resources.utils.decorators.clientDBConnection import fn_make_client_db_connection
from resources.utils.decorators.screenPermission import fn_check_screen_permission


class clsLkpActTaxType(Resource):

    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    def get(self, *args, **kwargs):
        try:
            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                'sproc_act_lkp_tax_type')
            sproc_result_sets = fn_sproc_response(cursor)
            return {'status': 'Success',
                    'data': sproc_result_sets,
                    'message': "Tax type data fetched successfully"
                   }, 200
        except Exception as e:
            return {'Error': str(e)}, 400

