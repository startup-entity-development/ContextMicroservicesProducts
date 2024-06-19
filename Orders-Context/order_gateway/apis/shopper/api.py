from flask import request
from flask_restful import Resource
import logging
from .validation import shopper_create_validation
from order_ctx_database_sqlalchemy_14.objects.shopper_object import ShopperDataBase, ShopperAttributesGateway
from apis.utils.serializer import serializer

log = logging.getLogger(__name__)

class ShopperApi(Resource):
    def post(self):
        """
        This endpoint creates new shopper.
        ---
        tags: ['Shopper']
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: Shopper
              required:
                - name
              properties:
                name:
                  type: string
                  description: Name of the shopper
        responses:
          201:
            description: Shopper created successfully
            schema:
              properties:
                shopper:
                  $ref: '#/schemas/Shopper'
          400:
            description: Invalid data provided
            schema:
              $ref: '#/schemas/Error'
        """
        try:
            data = request.get_json()
            if not shopper_create_validation(data):
                return {'error': 'Invalid data'}, 400
            
            try:
                shopper_attributes = ShopperAttributesGateway().from_dict(data)
            except Exception as e:
                return {'error': 'Invalid data'}, 400

            shopper_data_base = ShopperDataBase(log)
            shopper = shopper_data_base.create(shopper_attributes)
            return {'shopper': serializer(shopper.to_dict())}, 201

        except Exception as e:
            return {'error': str(e)}, 500
  