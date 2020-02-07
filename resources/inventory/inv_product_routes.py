# ~/mysql-flask-connector/resources/inventory/inv_product_routes.py

from .product import InvProduct

def inv_product_initialize_routes(api):
    api.add_resource(InvProduct, '/api/v1/product')