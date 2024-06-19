from mutations.cart_mutation import ObtainCart
from resolvers.cart_resolver import CartResolver

class ResolversCart(
    CartResolver
):
    """Queries which can be performed by this  API"""

class MutationCart:
    """Mutation which can be performed by this  API"""
    obtainCart = ObtainCart.Field()