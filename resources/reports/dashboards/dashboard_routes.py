# ~/mysql-flask-connector/resources/inventory/inv_routes.py

from .apiOrgRptDashboardClient import clsOrgClientDashboard

def fn_org_client_dashboard_initialize_routes(api):
    api.add_resource(clsOrgClientDashboard, '/api/v1/client-dashboard')