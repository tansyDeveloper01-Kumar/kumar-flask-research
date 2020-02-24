from flask_restful import Resource
from flask import request, Response, jsonify

from resources.db.executeSProc import fn_call_stored_procedure, fn_return_sproc_multiple_result_sets
from resources.utils.decorators.clientDBConnection import fn_make_client_db_connection
from resources.utils.decorators.screenPermission import fn_check_screen_permission


class clsSlsRptPdfSalesInvoice(Resource):

    @fn_make_client_db_connection()
    @fn_check_screen_permission()
    # get details to print PDF sales report listing
    def get(self, *args, **kwargs):
        try:
            entity_id = int(request.headers.get('entity_id'))
            debug_sproc = int(request.headers.get('debug_sproc'))
            audit_screen_visit = int(request.headers.get('audit_screen_visit'))

            input_params = [entity_id, kwargs['session_id'], kwargs['user_id'],
                            kwargs['screen_id'], debug_sproc, audit_screen_visit]

            output_params = [0, 0, 0]

            sproc_result_args, cursor = fn_call_stored_procedure(kwargs['client_db_connection'],
                                                                 'sproc_sls_rpt_pdf_sales_invoice',
                                                                 *input_params, *output_params)

            return fn_return_sproc_multiple_result_sets(sproc_result_args=sproc_result_args, cursor=cursor,
                                                        functionality="Sales invoice data fetched successfully")

        except Exception as e:
            return {'Error': str(e)}, 400

