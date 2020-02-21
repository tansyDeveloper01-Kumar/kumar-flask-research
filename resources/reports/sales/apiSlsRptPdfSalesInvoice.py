from flask_restful import Resource
from flask import request, Response, jsonify
import datetime
import json

from resources.db.executeSProc import fn_call_stored_procedure, fn_sproc_response
from resources.utils.decorators.clientDBConnection import fn_make_client_db_connection
from resources.utils.decorators.screenPermission import fn_check_screen_permission


class clsSlsRptPdfSalesInvoice(Resource):

    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    # get details to print PDF sales report listing
    def get(self, *args, **kwargs):
        try:
            entity_id = request.headers.get('entity_id')
            debug_sproc = request.headers.get('debug_sproc')
            audit_screen_visit = request.headers.get('audit_screen_visit')

            input_params = [entity_id, kwargs['session_id'], kwargs['user_id'],
                            kwargs['screen_id'], debug_sproc, audit_screen_visit]

            output_params = [0, 0, 0]

            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_sls_rpt_pdf_sales_invoice',
                                                                 *input_params, *output_params)

            sproc_result_args_type = isinstance(sproc_result_args, str)
            if sproc_result_args_type == True and cursor == 400:
                return {'status': 'Failure', 'data': sproc_result_args}, 400
            # sproc_result_args[5] = err_flag & sproc_result_args[7] = err_msg
            elif sproc_result_args[-3] == 1:
                return {'status': 'Failure', 'data': sproc_result_args[-2], 'error_step': sproc_result_args[-1]}, 200
            else:
                sproc_result = []
                for result in cursor.stored_results():
                    sproc_result.append(result.fetchall())

            return jsonify({"data": sproc_result})

        except Exception as e:
            return {'Error': str(e)}, 400

