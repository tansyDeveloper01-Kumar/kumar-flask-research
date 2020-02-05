from flask import Flask
from flask import Blueprint
from flask_restful import Api

from resources.Authenticate.Auth import AuthBackend

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(AuthBackend, '/login')

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)