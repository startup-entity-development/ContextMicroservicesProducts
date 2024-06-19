"""App entry point."""

from flask import Flask
from flask_mail import Mail
from graphql_server.flask import GraphQLView
from containers import Container
from core.order_email_sender import TextEmailSender
from schemas.schema_public import schema_public
from schemas.schema_protected import schema_protected
from api.email_protected import api as protected_api
from api.email_public import api as public_api
from dependency_injector.wiring import inject, Provide


def create_app() -> Flask:
    """Create Flask app."""
    container = Container()
    app = Flask(__name__, template_folder="templates")
    app.container = container
    container.wire(
        modules=[
            __name__,
            "api.email_protected",
            "api.email_public",
            "schemas.mutation_email_protected",
        ]
    )
    app.register_blueprint(public_api, url_prefix="/public/email")
    app.register_blueprint(protected_api, url_prefix="/protected/email")

    app.add_url_rule(
        "/protected/email/gateway_graphql",
        view_func=GraphQLView.as_view(
            "graphqlPortected",
            schema=schema_protected,
            graphiql=True,
        ),
    )

    app.add_url_rule(
        "/public/email/gateway_graphql",
        view_func=GraphQLView.as_view(
            "graphql",
            schema=schema_protected,
            graphiql=True,
        ),
    )

    app.config.from_pyfile("settings.py")

    mail: Mail = container.mail()
    mail.init_app(app)

    return app


if __name__ == "__main__":
    app_instance = create_app()
    app_instance.run(debug=True)
