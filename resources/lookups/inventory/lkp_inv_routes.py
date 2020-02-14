# ~/mysql-flask-connector/resources/lookups/inventory/lkp_inv_routes.py

from .apiInvLkpBrand import clsInvLkpBrand
from .apiInvLkpManufacture import clsInvLkpManufacture
from .apiInvLkpProductType import clsInvLkpProductType
from .apiInvLkpUnitOfMeasure import clsInvLkpUnitOfMeasure

def fn_lkp_inv_initialize_routes(api):
    api.add_resource(clsInvLkpBrand, '/api/lkp/v1/brand-items')
    api.add_resource(clsInvLkpManufacture, '/api/lkp/v1/manufacture')
    api.add_resource(clsInvLkpProductType, '/api/lkp/v1/product-type')
    api.add_resource(clsInvLkpUnitOfMeasure, '/api/lkp/v1/measure')