""" This module contains the mutation to create a order item. """

from datetime import datetime
import logging
import graphene
from graphql_relay import from_global_id
from order_ctx_database_sqlalchemy_14.models.cart import ModelCart
from order_ctx_database_sqlalchemy_14.objects.cart_object import CartDataBase
from order_ctx_database_sqlalchemy_14.objects.order_object import (
    OrderDataBase,
    OrderAttributesGateway,
)
from nodes.order_node import OrderNode
from services.order_email_service import resolve_send_order_email


class OrderGraphAttribute:
    """Attributes to create a Order item."""

    address = graphene.String(description="Address of the order", required=True)
    contact_number = graphene.String(
        description="Contact number of the order", required=True
    )
    note = graphene.String(description="Note related to the order", required=True)
    product_delivery_date = graphene.Date(
        description="Product delivery date of the order (YYYY-MM-DD)", required=True
    )
    cart_id = graphene.String(description="Cart id of the order", required=True)
    customer_name = graphene.String(description="Customer name of the order", required=True)
    customer_email = graphene.String(description="Customer email of the order", required=True)
    time_range = graphene.String(description="Time range of the order delivery", required=True)


class OrderGraphInput(graphene.InputObjectType, OrderGraphAttribute):
    """Arguments to create a Cart item."""


class CreateOrder(graphene.Mutation):
    """Create a Order item."""

    order = graphene.Field(
        lambda: OrderNode, description="Order item created by this mutation."
    )

    class Arguments:
        order_input = OrderGraphInput(required=True)

    def mutate(self, info, order_input):

        log = logging.getLogger(__name__)
        try:
            order_input["shopper_id"] = 1
            cart_id = from_global_id(order_input.cart_id).id
            
            if not cart_id:
                raise Exception(f"Invalid Cart Id")
            order_input["cart_id"] = int(cart_id)

            # Instantiate the cart database object
            cart_db: CartDataBase = CartDataBase(log)

            # Get cart details
            cart: ModelCart = cart_db.get(cart_id)
            if not cart:
                raise Exception("Invalid cart")

            # Deactive the cart

            cart.deactive_date = datetime.now()
            order_input["user_account_id"] = cart.user_account_id
            order_attributes = OrderAttributesGateway().from_dict(order_input)

            # Update counter promotion. 
            
            
            
            
            
            
        except Exception as e:
            raise Exception(f"Error in CartItemGraphInput: {e}")

        # Instantiate the order database object
        order_db: OrderDataBase = OrderDataBase(log)

        try:
            order_model = order_db.get_order_by_cart_id(cart_id=cart_id)
            if not order_model:
                order_model = order_db.create(
                    order=order_attributes, raise_integrety_except=True
                )
                order_db.db_session.refresh(order_model)
            else:
                order_model = order_db.update(
                    order_id=order_model.id,
                    order=order_attributes,
                    raise_integrety_except=True,
                )

        except Exception as e:
            order_db.db_session.rollback()
            raise Exception(f"Error in create order: {e}")
        try:
            # TODO: Temporal solution for calculating cart total inside cart object
            log.info(f"call resolve_send_order_email")
            resolve_send_order_email(
                order=order_model,
                cart=cart,
                customer_name=order_input.customer_name,
                customer_email=order_input.customer_email,
                time_range=order_input.time_range,
                log=log,
                )
        except Exception as e:
            log.error(f"Error in sending order email: {e}")
            raise Exception(f"Error in sending order email: {e}")

        return CreateOrder(order=order_model)
