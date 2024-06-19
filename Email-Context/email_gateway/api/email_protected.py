"""Protected API for email gateway"""

from flask import Blueprint, request
from dependency_injector.wiring import inject, Provide
from containers import Container
from core.order_email_sender import OrderEmailSender
from core.model.cart_order import CartOrder

api = Blueprint("protected_api", __name__)


@api.post("")
@inject
def email(
    email_sender: OrderEmailSender = Provide[Container.order_email_sender],
):
    """Sends email
    Returns:
        dict: Whether the email was sent successfully
    """
    order = CartOrder(**request.get_json())
    return email_sender.send_order_email(order=order)
