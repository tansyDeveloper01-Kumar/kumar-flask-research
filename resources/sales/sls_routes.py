from .salesInvoice import clsSlsInvoice

def fn_sls_invoice_initialize_routes(api):
    api.add_resource(clsSlsInvoice, '/api/v1/sales-invoice')