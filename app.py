from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

from resources.authenticate.sys_auth_routes import sys_auth_initialize_routes
from resources.inventory.inv_product_routes import inv_product_initialize_routes
from resources.lookups.inventory.lkp_inv_routes import lkp_inv_initialize_routes

app = Flask(__name__)
api = Api(app)

# Route
sys_auth_initialize_routes(api)
inv_product_initialize_routes(api)
lkp_inv_initialize_routes(api)

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)