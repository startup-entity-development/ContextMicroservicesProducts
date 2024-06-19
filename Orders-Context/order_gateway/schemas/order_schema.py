from mutations.order_mutation import CreateOrder
from resolvers.order_resolver import OrderResolver
    
class ResolversOrder(
    OrderResolver
):
    """Queries which can be performed by this  API"""
class MutationOrder:
    create_order = CreateOrder.Field()