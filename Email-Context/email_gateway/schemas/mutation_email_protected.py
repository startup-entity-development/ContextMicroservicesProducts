""" The protected mutations for sending emails """

import logging
from graphene import Mutation, Field
from dependency_injector.wiring import inject, Provide
from containers import Container
from core.order_email_sender import OrderEmailSender, TextEmailSender
from core.model.cart_order import CartOrder
from schemas.type.cart_order_input import CartOrderInput, EmailTextInput
from schemas.type.response import Response


class SendCartOrderEmailMutation(Mutation):
    """The mutation to send a cart order email"""

    class Arguments:
        """The arguments for the SendCartOrderEmail mutation"""

        order_input = CartOrderInput(required=True)

    response = Field(lambda: Response)

    @inject
    def mutate(
        self,
        info,
        order_input: CartOrderInput,
        email_sender: OrderEmailSender = Provide[Container.order_email_sender],
    ):
        log = logging.getLogger(__name__)

        """The mutation to send a cart order email"""
        message = f"Email sent successfully to {order_input.customer_details.email}"
        response = Response(message=message)
        try:
            log.info("Sending email to %s", order_input.customer_details.email)
            email_sender.send_order_email(order=CartOrder(**order_input))
            log.info("Email sent to %s", order_input.customer_details.email)
        except Exception as error:
            log.exception("Failed to send email, %s", str(error))
            response.message = f"Failed to send email: {str(error)}"
        return SendCartOrderEmailMutation(response=response)

class SendtextEmailMutation(Mutation):
    """The mutation to send a cart order email"""

    class Arguments:
        """The arguments for the SendCartOrderEmail mutation"""
        email_text_input = EmailTextInput(required=True)

    response = Field(lambda: Response)

    @inject
    def mutate(
        self,
        info,
        email_text_input: EmailTextInput,
        email_sender: TextEmailSender = Provide[Container.text_email_sender],
    ):
        log = logging.getLogger(__name__)

        """The mutation to send a cart order email"""
        response = Response(message="message")
        try:
            log.info("Sending email to %s", email_text_input.recipient)
            email_sender.send_text_email(body=email_text_input.body,
                                         subject=email_text_input.subject, 
                                         recipients=email_text_input.recipient)
            log.info("Email sent to %s", email_text_input.recipient)
        except Exception as error:
            log.exception("Failed to send email, %s", str(error))
            response.message = f"Failed to send email: {str(error)}"
        return SendtextEmailMutation(response=response)