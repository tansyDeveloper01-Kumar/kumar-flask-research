# ~/mysql-flask-connector/resources/lookups/inventory/lkp_inv_routes.py

from .apiLkpOrgAccount import clsLkpOrgAccount


def lkp_org_initialize_routes(api):
    api.add_resource(clsLkpOrgAccount, '/api/lkp/v1/account')