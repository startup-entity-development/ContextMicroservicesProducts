from flask import request
from flask_restful import Resource
import logging
from .validation import order_create_validation
from order_ctx_database_sqlalchemy_14.objects.order_object import OrderDataBase, OrderAttributesGateway
from order_ctx_database_sqlalchemy_14.objects.shopper_object import ShopperDataBase
from order_ctx_database_sqlalchemy_14.objects.cart_object import CartDataBase
from datetime import datetime
from apis.utils.serializer import serializer

log = logging.getLogger(__name__)

class OrderApi(Resource):
    def post(self):
        """
        This endpoint creates new order.
        ---
        tags: ['Order']
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: Order
              required:
                - address
                - contact_number
                - shopper_id
                - cart_id
              properties:
                address:
                  type: string
                  description: Address of the order
                contact_number:
                  type: string
                  description: Contact number of the order
                note:
                  type: string
                  description: Note of the order
                product_delivery_date:
                  type: string
                  description: Product delivery date of the order
                  example: '2024-12-25'
                shopper_id:
                  type: string
                  description: Shopper of the order
                cart_id:
                  type: string
                  description: Cart of the order
        responses:
          201:
            description: Order created successfully
            schema:
              order:
                $ref: '#/schemas/Order'
          400:
            description: Invalid data provided
            schema:
              $ref: '#/schemas/Error'
        """
        try:
            data = request.get_json()
            error_validations = order_create_validation(data)
            if not error_validations["is_valid_data"]:
                return {"errors": error_validations["errors"]}, 400
            
            try:
                order_attributes = OrderAttributesGateway().from_dict(data)
            except Exception as e:
                return {'error': 'Invalid data'}, 400

            cart_database = CartDataBase(log)
            cart = cart_database.get(data['cart_id'])
            if not cart:
                return {'error': 'Cart not found'}, 404
            
            shopper_database = ShopperDataBase(log)
            shipper = shopper_database.get(data['shopper_id'])
            if not shipper:
                return {'error': 'Shopper not found'}, 404

            order_data_base = OrderDataBase(log)
            order = order_data_base.create(order_attributes)

            return {'order': serializer(order.to_dict())}, 201

        except Exception as e:
            return {'error': str(e)}, 500
  