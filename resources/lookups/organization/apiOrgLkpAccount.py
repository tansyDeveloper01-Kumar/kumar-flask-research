from flask_restful import Resource
from flask import request

from resources.db.executeSProc import fn_call_stored_procedure, fn_return_sproc_single_result_sets
from resources.utils.decorators.clientDBConnection import fn_make_client_db_connection
from resources.utils.decorators.screenPermission import fn_check_screen_permission
from resources.db.dbConnect import fn_close_db_connection
import datetime

class clsLkpOrgAccount(Resource):

    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    def get(self, *args, **kwargs):
        try:
            print("+++++++++++++++ Account lookup +++++++++++++++")
            print("start time for account lookup", datetime.datetime.now())
            debug_sproc = int(request.headers.get('debug_sproc'))
            audit_screen_visit = int(request.headers.get('audit_screen_visit'))

            input_params = [kwargs['session_id'],kwargs['user_id'],kwargs['screen_id'], debug_sproc, audit_screen_visit]
            output_params = [0, 0, 0]
            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                'sproc_org_lkp_account',
                                                                *input_params,
                                                                *output_params)

            
            print("end time for account lookup", datetime.datetime.now())   
            return fn_return_sproc_single_result_sets(sproc_result_args=sproc_result_args, cursor=cursor,
                                                      functionality="Account data fetched successfully")
        except Exception as e:
            return {'Error': str(e)}, 400 

