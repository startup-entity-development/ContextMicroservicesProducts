from flask import Flask, request
from graphql_server.flask import GraphQLView
from schemas.schema_protected import schema_protected
from order_ctx_database_sqlalchemy_14.models.base import db_session
from flask import Blueprint
from private_api import api_protected as api_protected

app = Flask(__name__)

app.register_blueprint(api_protected, url_prefix='/protected/order')

app.add_url_rule('/protected/order/gateway_graphql', view_func=GraphQLView.as_view(
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
    app.run(debug=True, port=5001)