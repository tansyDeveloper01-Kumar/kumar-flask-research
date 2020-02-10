from flask_restful import Resource
from flask import request

from resources.db.switchDatabase import connect_to_database, is_token_valid

from resources.db.procedure import call_stored_procedure, sproc_response, \
                                   error_response

from resources.utils.decorators.screenPermission import check_screen_permission
from resources.utils.decorators.authVerification import check_auth_verification

class OrgClientDashboard(Resource):

    @check_screen_permission(screen_name = "products")
    @check_auth_verification()
    def get(self, *args, **kwargs):
        try:
            data = request.get_json()

            start_date = data.get('start_date')
            end_date = data.get('end_date')
            client_entity_id = int(data.get('client_entity_id'))

            iparams = [start_date, end_date, client_entity_id,
                       request.headers.get('session_id'),
                       request.headers.get('user_id'), 110001, 1, 1]

            oparams = [None, None, None, None,None, None, None, None,None,None,None]

            result_args, cursor = call_stored_procedure(kwargs['client_db_connection'], 
                                                    'sproc_org_rpt_dashboard_client',
                                                    *iparams, *oparams)
            
            sproc_result = []
            for result in cursor.stored_results():
                sproc_result.append(result.fetchall())
                        
            return {'status': 'Success', 'brands': sproc_result}, 200
            
        except Exception as e:
            return {'Error': str(e)}, 400
