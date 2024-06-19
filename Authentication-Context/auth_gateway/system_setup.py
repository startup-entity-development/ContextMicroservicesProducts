from flask import Blueprint

from authorization_management.authorization_middleware import require_permission_internal
from database_setup import create_database_auth

api = Blueprint('private_api', __name__)

@api.post('/create_database')
@require_permission_internal(root_user=True)
def create_database():
    result = create_database_auth(interactive=False)
    return result

