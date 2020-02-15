from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

from resources.authenticate.sys_auth_routes import fn_sys_auth_initialize_routes
from resources.inventory.inv_product_routes import fn_inv_product_initialize_routes
from resources.dashboards.dashboard_routes import fn_org_client_dashboard_initialize_routes
from resources.sales.sls_routes import fn_sls_invoice_initialize_routes
from resources.reports.sales.sales_routes import fn_reports_initialize_routes

# Lookups paths
from resources.lookups.inventory.lkp_inv_routes import fn_lkp_inv_initialize_routes
from resources.lookups.organization.lkp_org_routes import fn_lkp_org_initialize_routes
from resources.lookups.account.lkp_act_routes import fn_lkp_act_initialize_routes

app = Flask(__name__)
api = Api(app)

# Route
fn_sys_auth_initialize_routes(api)
fn_inv_product_initialize_routes(api)
fn_org_client_dashboard_initialize_routes(api)
fn_sls_invoice_initialize_routes(api)
fn_reports_initialize_routes(api)

fn_lkp_inv_initialize_routes(api)
fn_lkp_org_initialize_routes(api)
fn_lkp_act_initialize_routes(api)

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)