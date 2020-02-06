from flask import Flask
from flask import Blueprint
from flask_restful import Api
from dotenv import load_dotenv

from resources.Authenticate.Auth import AuthBackend
from resources.inventory.product import InvProduct

from resources.lookups.inventory.brand import LookupInvBrand
from resources.lookups.inventory.productType import LookupInvProductType
from resources.lookups.inventory.manufacture import LookupInvManufacture
from resources.lookups.inventory.unitOfMeasure import LookupInvUnitOfMeasure
from resources.lookups.inventory.account import LookupInvAccount


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

app = Flask(__name__)

app.register_blueprint(api_bp, url_prefix='/api')

# Route
api.add_resource(AuthBackend, '/v1/login')
api.add_resource(InvProduct, '/v1/product')

api.add_resource(LookupInvBrand, '/v1/brand-items')
api.add_resource(LookupInvProductType, '/v1/product-type')
api.add_resource(LookupInvManufacture, '/v1/manufacture')
api.add_resource(LookupInvUnitOfMeasure, '/v1/measure')
api.add_resource(LookupInvAccount, '/v1/account')



if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)