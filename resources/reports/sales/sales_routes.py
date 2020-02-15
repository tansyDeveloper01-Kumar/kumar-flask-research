# ~/mysql-flask-connector/resources/inventory/inv_product_routes.py

from .apiSlsRptPdfSalesInvoice import clsSlsRptPdfSalesInvoice

def fn_reports_initialize_routes(api):
    api.add_resource(clsSlsRptPdfSalesInvoice, '/api/v1/sales-invoice-report')