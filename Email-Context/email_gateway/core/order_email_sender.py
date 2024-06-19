from flask import render_template
from core.email_sender import EmailSender
from core.model.cart_order import CartOrder


class OrderEmailSender(EmailSender):
    """The class to send a cart order email"""

    def send_order_email(self, order: CartOrder):
        """The method to send a cart order email"""
        template = self.__get_template(order)
        subject = f" Purchase # {order.order_id} Receipt"
        recipient = order.customer_details.email
        return self.send_email(
            template=template,
            subject=subject,
            recipients=[recipient, "denisbueltan@gmail.com",],
        )

    def __get_template(self, order):
        return render_template(
            "cart_order_email.html",
            order=order,
        )


class TextEmailSender(EmailSender):
    """The class to send a cart order email"""

    def send_order_email(self, body:str, subject:str, recipient:str):
        subject =   subject
        recipient = recipient
        return self.send_text_email(
            body=body,
            subject=subject,
            recipients=[recipient,],
        )
