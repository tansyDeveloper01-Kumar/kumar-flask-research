from flask_restful import Resource
from flask import request

from resources.db.dbConnect import connect_to_database, is_token_valid

from resources.db.executeSProc import call_stored_procedure, sproc_response, \
                                   error_response

from resources.utils.decorators.screenPermission import check_screen_permission
from resources.utils.decorators.authVerification import check_auth_verification


class clsInvLkpBrand(Resource):

    @check_screen_permission(screen_name = "products")
    @check_auth_verification()
    def get(self, *args, **kwargs):
        try:
            result_args, cursor = call_stored_procedure(kwargs['client_db_connection'], 
                                                    'sproc_inv_lkp_brand',
                                                    request.headers.get('session_id'), 
                                                    request.headers.get('user_id'),
                                                    110001, 1, 1, 0, 0, 0)
            sproc_result = sproc_response(cursor)
            if not sproc_result:
                return error_response(code=404, type='Not Found', message='Brands not found', fbtrace_id=None), 404
            dropdown_data = [{'brand_id': each_product[0], 'brand': each_product[1]} for each_product in sproc_result]
            
            return {'status': 'Success', 'brands': dropdown_data}, 200
            
        except Exception as e:
            return {'Error': str(e)}, 400
        
