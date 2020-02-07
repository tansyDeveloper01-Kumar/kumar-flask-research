from flask_restful import Resource
from flask import request
from mysql.connector import Error

import mysql.connector
import os

from resources.db.switchDatabase import connect_to_database, is_token_valid

from resources.db.procedure import call_stored_procedure, sproc_response, \
                                   error_response


class InvProduct(Resource):
    def get(self):
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
                                                    'sproc_inv_product_grid',
                                                    request.headers.get('session_id'), 
                                                    request.headers.get('user_id'),
                                                    110001, 1, 1, 0, 0, 0)
            sproc_result = sproc_response(cursor)
            if not sproc_result:
                return error_response(code=404, type='Not Found', 
                                      message='product not found', 
                                      fbtrace_id=None), 404

            dropdown_data = [{'product': each_product[0], 'product_type': each_product[1], 'entity_id': each_product[4]}
                                for each_product in sproc_result]
            
            return {'status': 'Success', 'brands': dropdown_data}, 200
            
        except Exception as e:
            return {'Error': str(e)}, 400
        
    def post(self):
        try:
            data = request.get_json()
            token = request.headers.get('token')
            sproc_result_array, result_args = is_token_valid(token)
            client_db_details = [sproc_result for sproc_result in sproc_result_array[0]]
            
            client_db_connection = connect_to_database(user=client_db_details[2], 
                                                       password=client_db_details[3],
                                                       database=client_db_details[1],
                                                       host=client_db_details[4])

            
            input_params = [data.get('isactive'), data.get('product_type_id'), data.get('product_name'),
                            data.get('brand_id'),
                            data.get('uom_type_id'), data.get('unit_content'), data.get('product_dimensions'),
                            data.get('isreturnable_item'), data.get('selling_price'), data.get('ledger_account_entity_id'),
                            data.get('maintain_inventory_flag'),
                            data.get('opening_stock'), data.get('re_order_level'), data.get('start_reminder_months'),
                            data.get('stop_reminder_months'), data.get('max_reminder_count'), data.get('reminder_sms_text'),
                            data.get('reminder_email_text')]

            result_args, cursor = call_stored_procedure(client_db_connection, 
                                                        'sproc_inv_product_dml_ins', 
                                                        *input_params,
                                                        request.headers.get('session_id'),
                                                        request.headers.get('user_id'), 
                                                        40004, 1, 1, 0, 0, 0)

            print('Result args: ', result_args[-3: -2])
            if result_args[-3: -2][0] is not None:
                return error_response(code=400, type='Bad Request', 
                                      message=result_args[-1:][0], 
                                      fbtrace_id=None), 400

            return {'message': 'Product added successfully'}, 201
            
        except Exception as e:
            return {'Error': str(e)}, 400

        
    def put(self):
        try:
            data = request.get_json()
            token = request.headers.get('token')
            
            sproc_result_array, result_args = is_token_valid(token)
            client_db_details = [sproc_result for sproc_result in sproc_result_array[0]]
            
            client_db_connection = connect_to_database(user=client_db_details[2], 
                                                       password=client_db_details[3],
                                                       database=client_db_details[1],
                                                       host=client_db_details[4])

            
            input_params = [data.get('entity_id'), data.get('isactive'), data.get('product_type_id'), 
                            data.get('product_name'), data.get('brand_id'),data.get('uom_type_id'),
                            data.get('unit_content'), data.get('product_dimensions'),
                            data.get('isreturnable_item'), data.get('selling_price'), 
                            data.get('ledger_account_entity_id'),data.get('maintain_inventory_flag'),
                            data.get('opening_stock'), data.get('re_order_level'), 
                            data.get('start_reminder_months'),data.get('stop_reminder_months'), 
                            data.get('max_reminder_count'), data.get('reminder_sms_text'),
                            data.get('reminder_email_text')]

            result_args, cursor = call_stored_procedure(client_db_connection, 
                                                        'sproc_inv_product_dml_upd', 
                                                        *input_params,
                                                        request.headers.get('session_id'),
                                                        request.headers.get('user_id'), 
                                                        40004, 1, 1, 0, 0, 0)

            print('Result args: ', result_args[-3: -2])
            if result_args[-3: -2][0] is not None:
                return error_response(code=400, type='Bad Request', 
                                      message=result_args[-1:][0], 
                                      fbtrace_id=None), 400

            return {'message': 'Product update successfully'}, 201
            
        except Exception as e:
            return {'Error': str(e)}, 400

        
    def delete(self):
        try:
            data = request.get_json()
            token = request.headers.get('token')
            
            sproc_result_array, result_args = is_token_valid(token)
            client_db_details = [sproc_result for sproc_result in sproc_result_array[0]]
            
            client_db_connection = connect_to_database(user=client_db_details[2], 
                                                       password=client_db_details[3],
                                                       database=client_db_details[1],
                                                       host=client_db_details[4])

            args = []
            conn = client_db_connection.cursor()
            conn.callproc('sproc_inv_product_dml_del_v1')
            # res = conn.fetchall()
            
            
            if result_args[-3: -2][0] is not None:
                return error_response(code=400, type='Bad Request', 
                                      message=result_args[-1:][0], 
                                      fbtrace_id=None), 400

            return {'message': 'Product deleted successfully'}, 201            
        except Exception as e:
            return {'Error': str(e)}, 400