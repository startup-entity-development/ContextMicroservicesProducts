import logging
from flask import Blueprint
from order_ctx_database_sqlalchemy_14.objects.shopper_object import ShopperDataBase
from middleware_authorization import require_permission_external
from setup_database import create_database_auth
api_protected = Blueprint('private_api', __name__)

@api_protected.post('/create_database')
@require_permission_external(root_user=True)
def create_database():
    result = create_database_auth(interactive=False)
    return result

def assign_admin_permission():
    pass


@api_protected.post('/create_default_shopper')
@require_permission_external(root_user=True)
def create_default_shopper():
    log = logging.getLogger(__name__)
    try:
        shopper_db = ShopperDataBase(log=log)
        shopper_db.create_default_shoppers()
    except Exception as e:
        raise Exception(f"Error in create_default_shopper: {e}")
    return "Shopper created successfully"

