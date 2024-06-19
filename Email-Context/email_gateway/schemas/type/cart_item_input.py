""" This module contains the cart item input type"""
from graphene import InputObjectType, String, Int, Float


class CartItemInput(InputObjectType):
    """Cart Item input type"""

    product_name = String(required=True)
    brand = String(required=True)
    description = String(required=True)
    image = String(required=True)
    size = String(required=True)
    quantity = Int(required=True)
    price = Float(required=True)
