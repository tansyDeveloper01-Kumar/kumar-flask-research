from flask import Flask
from flask import Blueprint
from flask_restful import Api
from dotenv import load_dotenv

from resources.Authenticate.Auth import AuthBackend
from resources.lookups.inventory.brand import LookupInvBrand

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

app = Flask(__name__)

app.register_blueprint(api_bp, url_prefix='/api/v1')

# Route
api.add_resource(AuthBackend, '/login')
api.add_resource(LookupInvBrand, '/brand-items')


if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)