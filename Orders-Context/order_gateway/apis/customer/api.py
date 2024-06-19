from flask import request
from flask_restful import Resource
import logging
from .validation import customer_create_validation
from order_ctx_database_sqlalchemy_14.objects.customer_object import CustomerDataBase, CustomerAttributesGateway
from apis.utils.serializer import serializer

log = logging.getLogger(__name__)

class CustomerApi(Resource):
    def post(self):
        """
        This endpoint creates new customer.
        ---
        tags: ['Customer']
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: Customer
              required:
                - name
              properties:
                name:
                  type: string
                  description: Name of the customer
                stripe_customer_id:
                  type: string
                  description: Stripe id of the customer
        responses:
          201:
            description: Customer created successfully
            schema:
              properties:
                customer:
                  $ref: '#/schemas/Customer'
          400:
            description: Invalid data provided
            schema:
              $ref: '#/schemas/Error'
        """
        try:
            data = request.get_json()
            if not customer_create_validation(data):
                return {'error': 'Invalid data'}, 400

            try:
                shopper_attributes = CustomerAttributesGateway().from_dict(data)
            except Exception as e:
                return {'error': 'Invalid data'}, 400

            customer_data_base = CustomerDataBase(log)
            customer = customer_data_base.create(shopper_attributes, raise_integrety_except=True)
            return {'customer': serializer(customer.to_dict())}, 201

        except Exception as e:
            return {'error': str(e)}, 500
  