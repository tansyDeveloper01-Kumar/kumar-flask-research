from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

# Crypto
# from resources.utils.crypto.sys_crypto_routes import sys_crypto_routes

from resources.authenticate.sys_auth_routes import sys_auth_initialize_routes
# from resources.inventory.inv_product_routes import inv_product_initialize_routes
# from resources.dashboards.dashboard_routes import org_client_dashboard_initialize_routes

# Lookups paths
# from resources.lookups.inventory.lkp_inv_routes import lkp_inv_initialize_routes
# from resources.lookups.organization.lkp_org_routes import lkp_org_initialize_routes

app = Flask(__name__)
api = Api(app)

# Route
# sys_crypto_routes(api)
sys_auth_initialize_routes(api)
# inv_product_initialize_routes(api)
# org_client_dashboard_initialize_routes(api)

# lkp_inv_initialize_routes(api)
# lkp_org_initialize_routes(api)

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)