"""Containers module."""

from dependency_injector import containers, providers
from flask_mail import Mail
from core.order_email_sender import OrderEmailSender, TextEmailSender


class Container(containers.DeclarativeContainer):
    """App container."""

    mail = providers.Singleton(Mail)
    order_email_sender = providers.Factory(
        OrderEmailSender,
        mail=mail,
    )
    text_email_sender = providers.Factory(
        TextEmailSender,
        mail=mail,)
