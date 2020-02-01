from flask import Blueprint, request, jsonify

from utils.error_response import error_response
from utils.stored_procedures import *

from flask_restx import Api, Resource

product_module = Blueprint("product_module", __name__)

api = Api(product_module, doc='/docs')

namespace = api.namespace('Product', 
                           description='Products operations', 
                           path='/api_inv_product'
                         )

client_db_connection = None




@namespace.route('/products', methods=['GET', 'POST'])
class ProductsGrid(Resource):
    @staticmethod
    def get():
        print("Hello")
