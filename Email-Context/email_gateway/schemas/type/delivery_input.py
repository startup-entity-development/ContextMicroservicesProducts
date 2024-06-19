""" This module contains the delivery input type"""

from graphene import InputObjectType, String


class DeliveryInput(InputObjectType):
    """Delivery input type"""

    address = String(required=True)
    delivery_date = String(required=True)
    time_range = String(required=True)
