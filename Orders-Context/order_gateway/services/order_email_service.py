""" This module contains the business logic for connecting to the order email service. """

from logging import Logger
import os
from typing import List
import requests
from graphql_relay.node.node import to_global_id
from order_ctx_database_sqlalchemy_14.models.order import ModelOrder
from order_ctx_database_sqlalchemy_14.models.cart import ModelCart
from order_ctx_database_sqlalchemy_14.models.cart_product_detail import (
    ModelCartProductDetail,
)
from services.model.cart_order import CartOrder
from services.model.customer import Customer
from services.model.delivery import Delivery
from services.model.cart_item import CartItem
from services.product_service import resolve_getProductsByIds

from datetime import datetime
from pytz import timezone

tz = timezone("EST")
datetime.now(tz)


EMAIL_GATEWAY_HOST_NAME = os.environ.get("EMAIL_GATEWAY_HOST_NAME")
EMAIL_PROTECTED_SERVICE_URL = (
    f"{EMAIL_GATEWAY_HOST_NAME}/protected/email/gateway_graphql"
)


def resolve_send_order_email(
    order: ModelOrder,
    cart: ModelCart,
    customer_name: str,
    customer_email: str,
    time_range: str,
    log: Logger,
):
    """Send order email to the user."""
    try:
        cart_order = __get_cart_order_input(
            order, cart, customer_name, customer_email, time_range, log=log
        )
    except Exception as e:
        raise Exception(f"Error in getting cart order input: {e}")

    mutation = """
    mutation SendCartOrderEmail($orderInput: CartOrderInput!) {
      sendCartOrderEmail(orderInput: $orderInput) {
        response {
          message
          }
        }
      }
    """
    try:
        dict_cart_order = cart_order.to_dict()
    except Exception as e:
        raise Exception(f"Error in converting cart order to dict: {e}")

    variables = {"orderInput": dict_cart_order}
    try:
        log.info(f"before to call email service, variables: {variables} ")
        response = requests.post(
            EMAIL_PROTECTED_SERVICE_URL,
            json={"query": mutation, "variables": variables},
        )
        data = response.json()
        if response.status_code != 200:
            log.error(f"Error in sending order email status code !=200 : {data}")
            raise Exception(f"Error in sending order email status code !=200 : {data}")
    except Exception as e:
        log.exception(f"Error in sending order email: {e}")
        raise Exception(f"1 - Error in sending order email : {e}")
    except requests.exceptions as e:
        log.exception(f"Error in sending order email: {e}")
        raise Exception(f"2 - Error in sending order email: {e}")
    log.info(f"After request sending to Email Ctx response: {data} ")

    return data.get("data", {}).get("sendCartOrderEmail", {})


def __get_cart_order_input(
    order: ModelOrder,
    cart: ModelCart,
    customer_name: str,
    customer_email: str,
    time_range: str,
    log: Logger,
) -> CartOrder:
    """Get the cart order input."""
    try:
        customer_details = Customer(
            name=customer_name,
            email=customer_email,
            phone=order.contact_number,
        )
    except Exception as e:
        log.error(f"Error in getting customer details: {e}")
        raise Exception(f"Error in getting customer details: {e}")
    try:
        delivery_details = Delivery(
            address=order.address,
            delivery_date=order.product_delivery_date.strftime("%Y/%m/%d"),
            time_range=time_range,
        )
    except Exception as e:
        log.error(f"Error in getting delivery details: {e}")
        raise Exception(f"Error in getting delivery details: {e}")

    cart_products: List[ModelCartProductDetail] = [
        cart_product
        for cart_product in cart.cart_products_edge
        if cart_product.quantity > 0
    ]

    try:
        product_ids = [
            to_global_id("Product", cart_product.product_id)
            for cart_product in cart_products
        ]

    except Exception as e:
        raise Exception(f"Error in getting product ids: {e}")

    log.info(f"before to call resolve_getProductsByIds, product_ids: {product_ids} ")

    products = resolve_getProductsByIds(product_ids)
    log.info(f"after to call resolve_getProductsByIds, products: {products} ")

    order_details = []
    try:
        for count, item in enumerate(cart_products):
            description: str = products[count]["description"]
            # if size is not available then set it to "N/A"
            size: str = products[count]["size"] if products[count]["size"] else "N/A"
            # if brand is not available then set it to "N/A"
            brand: str = products[count]["brand"] if products[count]["brand"] else "N/A"
            order_details.append(
                CartItem(
                    quantity=item.quantity,
                    price=item.price,
                    product_name=products[count]["title"],
                    brand=brand,
                    description=description[:100] + (description[100:] and "..."),
                    image=products[count]["mediaEdge"]["edges"][0]["node"]["linkUrl"],
                    size=size,
                )
            )
    except Exception as e:
        raise Exception(f"Error in adding items in order_details {e}")

    log.info(f"order_details: {order_details} ")

    total = cart.calculate_sub_total()
    # TODO : TIME CREATE ORDER TEMPORARY SOLUTION
    # SAVE TIEMESTAMPS IN ORDER OBJECT (DATABESE)
    # AND DEFINE TIMEZONE IN ENVIRONMENT VARIABLES
    try:
        cart_order: CartOrder = CartOrder(
            order_id=str(order.id),
            created_date=datetime.now(tz).strftime("%Y/%m/%d"),
            created_time=datetime.now(tz).strftime("%I:%M %p"),
            total=total,
            customer_details=customer_details,
            delivery_details=delivery_details,
            order_details=order_details,
            notes=str(order.note),
        )
    except Exception as e:
        raise Exception(f"Error in creating cart order: {e}")
    return cart_order
