from flask_restful import Api
from flasgger import Swagger
from flask_cors import CORS
from .shopper.api import ShopperApi
from .customer.api import CustomerApi
from .cart.api import CartApi
from .cart_item.api import CartProductDetailApi
from .order.api import OrderApi

def create_restful_app(app):
    api = Api(app)

    #Allow cors
    CORS(app)
    
    Swagger(app, template_file='./apis/swagger_docs.yaml')

    api.add_resource(ShopperApi, '/api/shoppers', endpoint='create_shopper', methods=["post"])
    api.add_resource(CustomerApi, '/api/customers', endpoint='create_customer', methods=["post"])
    api.add_resource(CartApi, '/api/carts', endpoint='create_cart', methods=["post"])
    api.add_resource(CartProductDetailApi, '/api/cart_product_details', endpoint='create_cart_product_details', methods=["post"])
    api.add_resource(OrderApi, '/api/orders', endpoint='create_orders', methods=["post"])
    # api.add_resource(ShopperApi, '/api/shoppers/123', endpoint='patch123', methods=["patch"])

    return app