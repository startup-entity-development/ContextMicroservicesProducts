import graphene
from mutations.account_promotion import MutationsAccountPromotion
from resolver_protected.get_account_pricing_cart import ResolversAccountPricingCart


class QueryProtected(graphene.ObjectType,
            ResolversAccountPricingCart
            ):
    # node = graphene.relay.Node.Field()
    """Queries which can be performed by this API"""


class MutationProtected(graphene.ObjectType, 
                        MutationsAccountPromotion):
        """Mutations which can be performed by this API"""


schema_protected = graphene.Schema(query=QueryProtected , mutation=MutationProtected)