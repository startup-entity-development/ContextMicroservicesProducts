from flask import Flask
from graphql_server.flask import GraphQLView
from schemas.schema_public import schema_public
from schemas.schema_protected import schema_protected
from product_ctx_database_sqlalchemy_14.models.base import db_session
from flask import Blueprint
from private_api import api as private_api

app = Flask(__name__)
api_public = Blueprint('public_api', __name__)

# @api.get('/all')
# def public_get_product():
#     return {
#         'data':[
#             {
#                 'id': '7',
#                 'title': 'iPhone 9',
#                 'description': 'An apple mobile which is nothing like apple'
#             },
#             
#         ],
#     }, 200

app.register_blueprint(api_public, url_prefix='/public/product')
app.register_blueprint(private_api, url_prefix='/protected/product')

app.add_url_rule('/public/product/gateway_graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema_public,
    graphiql=True,
))


app.add_url_rule('/protected/product/gateway_graphql', view_func=GraphQLView.as_view(
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