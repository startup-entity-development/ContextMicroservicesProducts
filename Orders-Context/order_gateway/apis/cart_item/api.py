from flask import request
from flask_restful import Resource
import logging
from .validation import cart_item_create_validation
from apis.utils.serializer import serializer
from order_ctx_database_sqlalchemy_14.objects.cart_product_detail_object import CartProductDetailDataBase, CartProductDetailAttributesGateway
from order_ctx_database_sqlalchemy_14.objects.cart_object import CartDataBase
from datetime import datetime

log = logging.getLogger(__name__)

class CartProductDetailApi(Resource):
    def post(self):
        """
        This endpoint creates new cart item product.
        ---
        tags: ['CartProductDetail']
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: CartProductDetail
              required:
                - quantity
                - price
                - cost
                - cart_id
                - product_id
              properties:
                quantity:
                  type: integer
                  description: Quantity of cart product
                price:
                  type: integer
                  description: Quantity of cart product
                cost:
                  type: integer
                  description: Quantity of cart product
                cart_id:
                  type: integer
                  description: Id of cart
                product_id:
                  type: integer
                  description: Id of product
        responses:
          201:
            description: Cart product created successfully
            schema:
              properties:
                cart_product_detial:
                  $ref: '#/schemas/CartProductDetail'
          400:
            description: Invalid data provided
            schema:
              $ref: '#/schemas/Error'
        """
        try:
            data = request.get_json()
            error_validations = cart_item_create_validation(data)
            if not error_validations["is_valid_data"]:
                return {"errors": error_validations["errors"]}, 400

            try:
                cart_product_attributes = CartProductDetailAttributesGateway().from_dict(data)
            except Exception as e:
                return {'error': 'Invalid data'}, 400

            cart_id = data["cart_id"]
            cart_database = CartDataBase(log)
            cart = cart_database.get(cart_id)
            if not cart:
                return {'error': 'Cart not found'}, 404

            cart_product_database = CartProductDetailDataBase(log)
            cart_product_detail = cart_product_database.create(cart_product_attributes)

            if not cart_product_detail:
              return {'error': "Cart product not created"}, 500
            return {'cart_product_detail': serializer(cart_product_detail.to_dict())}, 201

        except Exception as e:
            return {'error': str(e)}, 500
