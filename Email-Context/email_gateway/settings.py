"""Flask configuration variables."""
from os import environ
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = "top-secret!"
MAIL_SERVER = "smtp.sendgrid.net"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = "apikey"
MAIL_PASSWORD = environ.get("SENDGRID_API_KEY")
MAIL_DEFAULT_SENDER = environ.get("MAIL_DEFAULT_SENDER")
USER_AUTH_ROOT = environ.get("USER_AUTH_ROOT", "root@authentication")
