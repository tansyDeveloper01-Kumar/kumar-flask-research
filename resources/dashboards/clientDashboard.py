from flask_restful import Resource
from flask import request

from resources.db.switchDatabase import connect_to_database, is_token_valid

from resources.db.procedure import call_stored_procedure, sproc_response, \
                                   error_response



class OrgClientDashboard(Resource):
    def get(self, *args):
        try:
            data = request.get_json()
            token = data.get('token')
            sproc_result_array, result_args = is_token_valid(token)
            client_db_details = [sproc_result for sproc_result in sproc_result_array[0]]
            
            client_db_connection = connect_to_database(user=client_db_details[2], 
                                                       password=client_db_details[3],
                                                       database=client_db_details[1],
                                                       host=client_db_details[4])
            
            result_args, cursor = call_stored_procedure(client_db_connection, 
                                                    'sproc_org_rpt_dashboard_client',
                                                    '2019-12-10','2019-12-10',84,
                                                    request.headers.get('session_id'), 
                                                    request.headers.get('user_id'),
                                                    110001, 1, 1, None, None, None, None,None, None, None, None,None,None,None)
            
            sproc_result = []
            for result in cursor.stored_results():
                sproc_result.append(result.fetchall())
                          
            return {'status': 'Success', 'brands': sproc_result}, 200
            
        except Exception as e:
            return {'Error': str(e)}, 400
