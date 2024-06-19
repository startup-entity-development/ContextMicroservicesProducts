import os
from flask import Flask
from graphql_server.flask import GraphQLView
from schemas.schema_public import schema_public
from schemas.schema_protected import schema_protected
from auth_model_sqlalchemy_14.base import db_session
from authentication_management.authentication_public import api as public_api
from system_setup import api as private_api
from authorization_management.authorization_public import api as public_api_authorization

app = Flask(__name__)
app.register_blueprint(public_api, url_prefix='/public/auth')
app.register_blueprint(private_api, url_prefix='/protected/auth')
app.register_blueprint(public_api_authorization, url_prefix='/public/auth')

app.add_url_rule('/protected/auth/gateway_graphql', view_func=GraphQLView.as_view(
    'graphqlPortected',
    schema=schema_protected,
    graphiql=True,
))


app.add_url_rule('/public/auth/gateway_graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema_public,
    graphiql=True,
))



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.close()
    
    
    
# Optional, for adding batch query support (used in Apollo-Client)
#app.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view(
#    'graphql',
#    schema=schema,
#    batch=True
#))

if __name__ == '__main__':
    app.run()