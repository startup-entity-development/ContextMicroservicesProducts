from flask import Blueprint
from middleware_authorization import require_permission_external
from setup_database import create_database_pricing

api = Blueprint('private_api', __name__)

@api.post('/create_database')
@require_permission_external(root_user=True)
def create_database():
    result = create_database_pricing(interactive=False)
    return result

