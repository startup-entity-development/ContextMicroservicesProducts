"""Protected schema of the API"""

from graphene import ObjectType, Schema, Field
from schemas.mutation_email_protected import SendCartOrderEmailMutation, SendtextEmailMutation
from schemas.type.response import Response


class QueryProtected(ObjectType):
    """Protected queries which can be performed by this API"""

    response = Field(Response)


class MutationProtected(ObjectType):
    """Protected mutations which can be performed by this API"""

    send_cart_order_email = SendCartOrderEmailMutation.Field()
    sent_text_email = SendtextEmailMutation.Field()


schema_protected = Schema(
    query=QueryProtected,
    mutation=MutationProtected,
)
