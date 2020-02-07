# ~/mysql-flask-connector/resources/lookups/inventory/lkp_inv_routes.py

from .account import LookupInvAccount
from .brand import LookupInvBrand
from .manufacture import LookupInvManufacture
from .productType import LookupInvProductType
from .unitOfMeasure import LookupInvUnitOfMeasure

def lkp_inv_initialize_routes(api):
    api.add_resource(LookupInvAccount, '/api/v1/account')
    api.add_resource(LookupInvBrand, '/api/v1/brand-items')
    api.add_resource(LookupInvManufacture, '/api/v1/manufacture')
    api.add_resource(LookupInvProductType, '/api/v1/product-type')
    api.add_resource(LookupInvUnitOfMeasure, '/api/v1/measure')