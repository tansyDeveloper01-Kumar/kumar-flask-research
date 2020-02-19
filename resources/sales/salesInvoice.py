from flask_restful import Resource
from flask import request, Response
import json
from datetime import datetime
import datetime

from resources.db.executeSProc import fn_call_stored_procedure, fn_return_sproc_status, \
                                      fn_return_sproc_single_result_sets, fn_return_sproc_ddl
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
            act_entity_id = request.headers.get('act_entity_id')
            debug_sproc = request.headers.get('debug_sproc')
            audit_screen_visit = request.headers.get('audit_screen_visit')

            output_params = [0, 0, 0]
            input_params = [int(act_entity_id), kwargs['session_id'], kwargs['user_id'], kwargs['screen_id'],
                            int(debug_sproc), int(audit_screen_visit)]
            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_sls_invoice_detail',
                                                                 *input_params,
                                                                 *output_params)

            sproc_result_args_type = isinstance(sproc_result_args, str)

            if sproc_result_args_type == True and cursor == 400:
                return {'status': 'Failure', 'data': sproc_result_args}, 400
            # sproc_result_args[5] = err_flag & sproc_result_args[7] = err_msg
            elif sproc_result_args[-3] == 1:
                return {'status': 'Failure', 'data': sproc_result_args[-1]}, 200
            else:
                sproc_result = []
                for result in cursor.stored_results():
                    sproc_result.append(result.fetchall())

                result = []
                for row in sproc_result[0][0]:
                    if isinstance(row, datetime.datetime):
                        date = row.strftime("%Y:%m:%d")
                        result.append(date)
                    else:
                        data = str(row)
                        result.append(data)
                return {'status': 'Success', 'product_details': result}, 200

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

            return fn_return_sproc_single_result_sets(sproc_result_args=sproc_result_args, cursor=cursor,
                                                      functionality="Sales invoice grid data Fetched successfully")

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

            return fn_return_sproc_ddl(sproc_result_args=sproc_result_args, cursor=cursor,
                                       functionality="Sales invoice saved successfully ")
        except Exception as e:
            return {'Error': str(e)}, 400


    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    def put(self, *args, **kwargs):
        try:
            data = request.get_json()

            debug_sproc = request.headers.get('debug_sproc')
            audit_screen_visit = request.headers.get('audit_screen_visit')

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
            debug_sproc = request.headers.get('debug_sproc')
            audit_screen_visit = request.headers.get('audit_screen_visit')

            output_params = [0, 0, 0]
            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_sls_invoice_dml_del',
                                                                 entity_id,
                                                                 kwargs['session_id'],
                                                                 kwargs['user_id'],
                                                                 kwargs['screen_id'],
                                                                 debug_sproc,
                                                                 audit_screen_visit,
                                                                 *output_params)

            return fn_return_sproc_ddl(sproc_result_args=sproc_result_args, cursor=cursor,
                                       functionality="Sales invoice deleted successfully ")
        except Exception as e:
            return {'Error': str(e)}, 400
