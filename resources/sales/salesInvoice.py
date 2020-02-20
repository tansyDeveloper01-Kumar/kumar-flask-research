from flask_restful import Resource
from flask import request, Response

from resources.db.executeSProc import fn_call_stored_procedure, fn_return_sproc_single_result_sets, \
                                      fn_return_sproc_ddl, fn_return_sproc_multiple_result_sets
from resources.utils.decorators.clientDBConnection import fn_make_client_db_connection
from resources.utils.decorators.screenPermission import fn_check_screen_permission

'''
Resource for getting sales invoice details
'''
class clsSlsInvoiceDetails(Resource):

    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    def get(self, *args, **kwargs):
        try:
            act_entity_id = int(request.headers.get('act_entity_id'))
            debug_sproc = int(request.headers.get('debug_sproc'))
            audit_screen_visit = int(request.headers.get('audit_screen_visit'))

            output_params = [0, 0, 0]
            input_params = [act_entity_id, kwargs['session_id'], kwargs['user_id'], kwargs['screen_id'],
                            debug_sproc, audit_screen_visit]
            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_sls_invoice_detail',
                                                                 *input_params,
                                                                 *output_params)

            return fn_return_sproc_multiple_result_sets(sproc_result_args=sproc_result_args, cursor=cursor,
                                                      functionality="Sales invoice details fetched successfully")
        except Exception as e:
            return {'Error': str(e)}, 400


'''
Resource for sales invoice CRUD
'''
class clsSlsInvoice(Resource):

    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    def get(self, *args, **kwargs):
        try:
            debug_sproc = int(request.headers.get('debug_sproc'))
            audit_screen_visit = int(request.headers.get('audit_screen_visit'))

            input_params = [kwargs['session_id'], kwargs['user_id'], kwargs['screen_id'],
                            debug_sproc, audit_screen_visit]
            output_params = [0, 0, 0]
            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_sls_invoice_grid',
                                                                 *input_params,
                                                                 *output_params)

            return fn_return_sproc_single_result_sets(sproc_result_args=sproc_result_args, cursor=cursor,
                                                      functionality="Sales invoice grid data Fetched successfully")

        except Exception as e:
            return {'Error': str(e)}, 400

    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    def post(self, *args, **kwargs):
        try:
            data = request.get_json()

            debug_sproc = int(request.headers.get('debug_sproc'))
            audit_screen_visit = int(request.headers.get('audit_screen_visit'))

            output_params = [0, 0, 0]
            input_params = [data.get('client_entity_id'), data.get('invoice_number'), data.get('invoice_date'),
                            data.get('invoice_due_date'), data.get('productEntityId_units_unitRate_taxTypeId_list'),
                            data.get('payment_terms_id'), data.get('discount_type_id'), data.get('discount_value'),
                            kwargs['session_id'],kwargs['user_id'],kwargs['screen_id'],debug_sproc, audit_screen_visit]

            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_sls_invoice_dml_ins',
                                                                 *input_params,
                                                                 *output_params)

            return fn_return_sproc_ddl(sproc_result_args=sproc_result_args, cursor=cursor,
                                       functionality="Sales invoice saved successfully ")
        except Exception as e:
            return {'Error': str(e)}, 400


    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    def put(self, *args, **kwargs):
        try:
            data = request.get_json()

            debug_sproc = int(request.headers.get('debug_sproc'))
            audit_screen_visit = int(request.headers.get('audit_screen_visit'))

            output_params = [0, 0, 0]
            input_params = [int(data.get('act_entity_id')),int(data.get('client_entity_id')), data.get('invoice_number'),
                            data.get('invoice_due_date'), data.get('productEntityId_units_unitRate_taxTypeId_list'),
                            int(data.get('invoice_status_id')),int(data.get('payment_terms_id')),int(data.get('discount_type_id')),
                            data.get('discount_value'),kwargs['session_id'], kwargs['user_id'], kwargs['screen_id'],
                            debug_sproc, audit_screen_visit]

            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_sls_invoice_dml_upd',
                                                                 *input_params,
                                                                 *output_params)

            return fn_return_sproc_ddl(sproc_result_args=sproc_result_args, cursor=cursor,
                                       functionality="Sales invoice updated successfully ")

        except Exception as e:
            return {'Error': str(e)}, 400


    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    def delete(self, *args, **kwargs):
        try:
            entity_id = int(request.headers.get('entity_id'))
            debug_sproc = int(request.headers.get('debug_sproc'))
            audit_screen_visit = int(request.headers.get('audit_screen_visit'))

            input_params = [entity_id, kwargs['session_id'], kwargs['user_id'], kwargs['screen_id'],
                            debug_sproc, audit_screen_visit]
            output_params = [0, 0, 0]
            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_sls_invoice_dml_del',
                                                                 *input_params,
                                                                 *output_params)

            return fn_return_sproc_ddl(sproc_result_args=sproc_result_args, cursor=cursor,
                                       functionality="Sales invoice deleted successfully ")
        except Exception as e:
            return {'Error': str(e)}, 400
