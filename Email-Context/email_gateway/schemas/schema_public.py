"""Public schema of the API"""

from graphene import ObjectType, Schema


class QueryPublic(ObjectType):
    """Public queries which can be performed by this API"""


class MutationPublic(ObjectType):
    """Public mutations which can be performed by this API"""


schema_public = Schema(
    query=QueryPublic,
    mutation=MutationPublic,
)
