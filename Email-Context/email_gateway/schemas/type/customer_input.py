""" This module contains the customer input type"""

from graphene import InputObjectType, String


class CustomerInput(InputObjectType):
    """Customer input type"""

    email = String(required=True)
    name = String(required=True)
    phone = String(required=True)
