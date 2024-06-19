"""This module contains the cart order input type"""
from graphene import InputObjectType, String, Float, List, NonNull
from schemas.type.customer_input import CustomerInput
from schemas.type.delivery_input import DeliveryInput
from schemas.type.cart_item_input import CartItemInput


class CartOrderInput(InputObjectType):
    """Cart order input type"""

    order_id = String(required=True)
    created_date = String(required=True)
    created_time = String(required=True)
    total = Float(required=True)
    notes = String()
    customer_details = CustomerInput(required=True)
    delivery_details = DeliveryInput(required=True)
    order_details = List(NonNull(CartItemInput))
    
class EmailTextInput(InputObjectType):
    """Cart order input type"""

    body = String(required=True)
    subject = String(required=True)
    recipient = String(required=True)
