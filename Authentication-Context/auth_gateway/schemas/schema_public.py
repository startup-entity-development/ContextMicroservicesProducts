import graphene
from schemas.schema_account import  PublicAccountMutations, PublicAccountResolvers


class QueryPublic(graphene.ObjectType,PublicAccountResolvers):
    
    # node = graphene.relay.Node.Field()
    """Queries which can be performed by this API"""

class MutationPublic(graphene.ObjectType, PublicAccountMutations,):
    """Mutations which can be performed by this API"""


schema_public = graphene.Schema(query=QueryPublic, mutation=MutationPublic)