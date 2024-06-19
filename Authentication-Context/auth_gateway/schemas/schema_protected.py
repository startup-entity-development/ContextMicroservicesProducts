import graphene
from schemas.schema_account import ProtectedAuthorizationMutations, ProtectedAccountResolvers, PublicAccountMutations, ProtectedAccountMutations
from schemas.schema_role_level import ProtectedMutationLevel, ProtectedMutationsRole, ProtectedLevelResolvers, ProtectedRoleResolvers


class QueryProtected(graphene.ObjectType,
            ProtectedRoleResolvers,
            ProtectedLevelResolvers,
            ProtectedAccountResolvers,
            ):
    
    # node = graphene.relay.Node.Field()
    """Queries which can be performed by this API"""

class MutationProtected(graphene.ObjectType,
                PublicAccountMutations,
                ProtectedAccountMutations,
                ProtectedMutationsRole,
                ProtectedMutationLevel,
                ProtectedAuthorizationMutations
                ):
    
    """Mutations which can be performed by this API"""


schema_protected = graphene.Schema(query=QueryProtected, mutation=MutationProtected)