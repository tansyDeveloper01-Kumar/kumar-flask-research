from .salesInvoice import clsSlsInvoice
from .salesInvoice import clsSlsInvoiceDetails

def fn_sls_invoice_initialize_routes(api):
    api.add_resource(clsSlsInvoice, '/api/v1/sales-invoice')
    api.add_resource(clsSlsInvoiceDetails, '/api/v1/sales-invoice-details')