from flask_restful import Resource
from flask import request

from resources.db.executeSProc import fn_call_stored_procedure, fn_sproc_response, fn_return_sproc_status
from resources.utils.decorators.clientDBConnection import fn_make_client_db_connection
from resources.utils.decorators.screenPermission import fn_check_screen_permission


class clsSlsInvoice(Resource):

    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    def get(self, *args, **kwargs):
        try:
            debug_sproc = request.headers.get('debug_sproc')
            audit_screen_visit = request.headers.get('audit_screen_visit')

            output_params = [0, 0, 0]
            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_sls_invoice_grid',
                                                                 kwargs['session_id'],
                                                                 kwargs['user_id'],
                                                                 kwargs['screen_id'],
                                                                 debug_sproc,
                                                                 audit_screen_visit,
                                                                 *output_params)

            return fn_return_sproc_status(sproc_result_args, cursor, "Sales Invoice ", "Fetched ")
        except Exception as e:
            return {'Error': str(e)}, 400

    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    def post(self, *args, **kwargs):
        try:
            data = request.get_json()

            debug_sproc = request.headers.get('debug_sproc')
            audit_screen_visit = request.headers.get('audit_screen_visit')

            output_params = [0, 0, 0]
            input_params = [data.get('client_entity_id'), data.get('invoice_number'), data.get('invoice_date'),
                            data.get('invoice_due_date'), data.get('productEntityId_units_unitRate_taxTypeId_list'),
                            data.get('payment_terms_id'), data.get('discount_type_id'), data.get('discount_value'),
                            kwargs['session_id'],kwargs['user_id'],kwargs['screen_id'],debug_sproc, audit_screen_visit]

            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_sls_invoice_dml_ins',
                                                                 *input_params,
                                                                 *output_params)

            sproc_result_args_type = isinstance(sproc_result_args, str)
            if sproc_result_args_type == True and cursor == 400:
                return {'status': 'Failure', 'data': sproc_result_args}, 400
            # sproc_result_args[5] = err_flag & sproc_result_args[7] = err_msg
            elif sproc_result_args[5] == 1:
                return {'status': 'Failure', 'data': sproc_result_args[7]}, 200
            else:
                return {'status': 'Success', 'data': "Product added successfully"}, 200

        except Exception as e:
            return {'Error': str(e)}, 400
