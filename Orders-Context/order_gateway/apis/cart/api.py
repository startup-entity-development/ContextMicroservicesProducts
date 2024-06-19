from flask import request
from flask_restful import Resource
from order_ctx_database_sqlalchemy_14.objects.cart_object import CartDataBase, CartAttributesGateway
from datetime import datetime
from apis.utils.serializer import serializer
import logging

log = logging.getLogger(__name__)

class CartApi(Resource):
    def post(self):
        """
        This endpoint creates new cart.
        ---
        tags: ['Cart']
        responses:
          201:
            description: Cart created successfully
            schema:
              properties:
                cart:
                  $ref: '#/schemas/Cart'
          400:
            description: Invalid data provided
            schema:
              $ref: '#/schemas/Error'
        """
        try:

            try:
                cart_attributes = CartAttributesGateway().from_dict({
                    "cart_total":0,
                    "total":0,
                    "delivery":0,
                    "tax":0,
                    "deactive_date":None
                })
            except Exception as e:
                return {'error': 'Invalid data'}, 400
            
            cart_data_base = CartDataBase(log)
            cart = cart_data_base.create(cart_attributes)

            if not cart:
              return {'error': "Cart not created"}, 500    

            return {'cart': serializer(cart.to_dict())}, 201

        except Exception as e:
            return {'error': str(e)}, 500
  