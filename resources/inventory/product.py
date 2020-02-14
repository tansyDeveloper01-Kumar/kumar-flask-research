from flask_restful import Resource
from flask import request

from resources.db.executeSProc import fn_call_stored_procedure, fn_sproc_response, fn_return_sproc_status
from resources.utils.decorators.clientDBConnection import fn_make_client_db_connection
from resources.utils.decorators.screenPermission import fn_check_screen_permission


class InvProductDetails(Resource):

    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    def get(self, *args, **kwargs):
        try:
            entity_id = request.headers.get('entity_id')
            debug_sproc = request.headers.get('debug_sproc')
            audit_screen_visit = request.headers.get('audit_screen_visit')

            output_params = [0, 0, 0]
            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_inv_product_detail',
                                                                 int(entity_id),
                                                                 kwargs['session_id'],
                                                                 kwargs['user_id'],
                                                                 kwargs['screen_id'],
                                                                 debug_sproc,
                                                                 audit_screen_visit,
                                                                 *output_params)

            sproc_result_args_type = isinstance(sproc_result_args, str)
            if sproc_result_args_type == True and cursor == 400:
                return {'status': 'Failure', 'data': sproc_result_args}, 400
            # sproc_result_args[5] = err_flag & sproc_result_args[7] = err_msg
            elif sproc_result_args[5] == 1:
                return {'status': 'Failure', 'data': sproc_result_args[7]}, 200
            else:
                sproc_result_sets = fn_sproc_response(cursor)

                product_details = [{'product': each_product[0],
                                    'product_type_entity_id': each_product[1],
                                    'unit_rate': str(each_product[2]),
                                    'start_reminder_months': each_product[3],
                                    'stop_reminder_months': each_product[4],
                                    'max_reminder_count': each_product[5],
                                    'product_type_entity_id': each_product[6],
                                    'product_entity_id': each_product[7],
                                    'active': each_product[8],
                                    'reminder_sms_text': each_product[9],
                                    'reminder_email_text': each_product[10],
                                    'uom_type_id': str(each_product[11]),
                                    'unit_content': str(each_product[12]),
                                    're_order_level': each_product[13],
                                    'maintain_inventory_flag': each_product[14],
                                    'brand_id': each_product[15]}
                                    for each_product in sproc_result_sets]

                return {'status': 'Success', 'product_details': product_details}, 200

        except Exception as e:
            return {'Error': str(e)}, 400



class InvProduct(Resource):

    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    def get(self, *args, **kwargs):
        try:
            debug_sproc = request.headers.get('debug_sproc')
            audit_screen_visit = request.headers.get('audit_screen_visit')

            account_lkp_output_params = [0, 0, 0]
            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_inv_product_grid',
                                                                 kwargs['session_id'],
                                                                 kwargs['user_id'],
                                                                 kwargs['screen_id'],
                                                                 debug_sproc,
                                                                 audit_screen_visit,
                                                                 *account_lkp_output_params)

            return fn_return_sproc_status(sproc_result_args, cursor, "Products ", "Fetched ")
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
            input_params = [data.get('isactive'), data.get('product_type_id'), data.get('product_name'),
                            data.get('brand_id'),data.get('uom_type_id'), data.get('unit_content'),
                            data.get('product_dimensions'),data.get('isreturnable_item'), data.get('selling_price'),
                            data.get('ledger_account_entity_id'),data.get('maintain_inventory_flag'),
                            data.get('opening_stock'), data.get('re_order_level'), data.get('start_reminder_months'),
                            data.get('stop_reminder_months'), data.get('max_reminder_count'),data.get('reminder_sms_text'),
                            data.get('reminder_email_text')]

            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_inv_product_dml_ins',
                                                                 *input_params,
                                                                 kwargs['session_id'],
                                                                 kwargs['user_id'],
                                                                 kwargs['screen_id'],
                                                                 debug_sproc,
                                                                 audit_screen_visit,
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


    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    def put(self, *args, **kwargs):
        try:
            data = request.get_json()

            debug_sproc = request.headers.get('debug_sproc')
            audit_screen_visit = request.headers.get('audit_screen_visit')

            output_params = [0, 0, 0]
            input_params = [data.get('entity_id'), data.get('isactive'), data.get('product_type_id'),
                            data.get('product_name'), data.get('brand_id'),data.get('uom_type_id'),
                            data.get('unit_content'), data.get('product_dimensions'),
                            data.get('isreturnable_item'), data.get('selling_price'), 
                            data.get('ledger_account_entity_id'),data.get('maintain_inventory_flag'),
                            data.get('opening_stock'), data.get('re_order_level'), 
                            data.get('start_reminder_months'),data.get('stop_reminder_months'), 
                            data.get('max_reminder_count'), data.get('reminder_sms_text'),
                            data.get('reminder_email_text')]

            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_inv_product_dml_upd',
                                                                 *input_params,
                                                                 kwargs['session_id'],
                                                                 kwargs['user_id'],
                                                                 kwargs['screen_id'],
                                                                 debug_sproc,
                                                                 audit_screen_visit,
                                                                 *output_params)

            sproc_result_args_type = isinstance(sproc_result_args, str)
            if sproc_result_args_type == True and cursor == 400:
                return {'status': 'Failure', 'data': sproc_result_args}, 400
            # sproc_result_args[5] = err_flag & sproc_result_args[7] = err_msg
            elif sproc_result_args[5] == 1:
                return {'status': 'Failure', 'data': sproc_result_args[7]}, 200
            else:
                return {'status': 'Success', 'data': "Product updated successfully"}, 201
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
                                                                 'sproc_inv_product_dml_del',
                                                                 entity_id,
                                                                 kwargs['session_id'],
                                                                 kwargs['user_id'],
                                                                 kwargs['screen_id'],
                                                                 debug_sproc,
                                                                 audit_screen_visit,
                                                                 *output_params)

            return fn_return_sproc_status(sproc_result_args, cursor, "Product ", "Deleted ")
        except Exception as e:
            return {'Error': str(e)}, 400
