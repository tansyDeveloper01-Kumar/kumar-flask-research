# ~/mysql-flask-connector/resources/inventory/inv_product_routes.py

from .clientDashboard import OrgClientDashboard

def fn_org_client_dashboard_initialize_routes(api):
    api.add_resource(OrgClientDashboard, '/api/v1/client-dashboard')