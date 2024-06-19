from flask import Flask
from graphql_server.flask import GraphQLView
from schemas.schema_protected import schema_protected
from flask import Blueprint
from system_setup import api as private_api
from pricing_ctx_database_sqlalchemy_14.models.base import db_session
app = Flask(__name__)
api_public = Blueprint('public_api', __name__)

app.register_blueprint(private_api, url_prefix='/protected/pricing')


app.add_url_rule('/protected/pricing/gateway_graphql', view_func=GraphQLView.as_view(
   'graphqlProtected',
   schema=schema_protected,
   graphiql=True,
))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# Optional, for adding batch query support (used in Apollo-Client)
# app.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view(
#    'graphql',
#    schema=schema,
#    batch=True
# ))

if __name__ == '__main__':
    app.run()