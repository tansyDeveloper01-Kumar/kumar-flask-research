# ~/mysql-flask-connector/resources/inventory/inv_routes.py

from .product import clsInvProduct, clsInvProductDetails

def fn_inv_product_initialize_routes(api):
    api.add_resource(clsInvProduct, '/api/v1/product')
    api.add_resource(clsInvProductDetails, '/api/v1/product-details')