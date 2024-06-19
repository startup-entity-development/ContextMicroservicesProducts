""" Email Service Module """

from flask_mail import Message, Mail


class EmailSender:
    """Class for sending emails"""

    def __init__(self, mail: Mail):
        """Constructor"""
        self.mail = mail

    def send_email(self, template, subject, recipients) -> dict:
        """Sends an email
        Args:
            template: The email template
            subject: The email subject
            recipients: The email recipients

        Returns:
            dict: Response indicating whether the email was sent successfully
        """
        message = Message(
            subject=subject,
            recipients=recipients,
        )
        message.html = template
        self.mail.send(message)
        return {
            "status": 200,
            "message": "Email sent successfully",
        }, 200

    def send_text_email(self, body, subject, recipients) -> dict:
        """Sends a text email
        Args:
            body: The email body
            subject: The email subject
            recipients: The email recipients

        Returns:
            dict: Response indicating whether the email was sent successfully
        """
        message = Message(
            subject=subject,
            recipients=[recipients],
        )
        message.body = body
        self.mail.send(message)
        return {
            "status": 200,
            "message": "Email sent successfully",
        }, 200