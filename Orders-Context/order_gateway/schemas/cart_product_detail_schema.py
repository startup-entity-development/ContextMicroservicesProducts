from mutations.cart_product_detail_mutation import CreateCartProductDetail
from resolvers.cart_product_detail_resolver import CartProductDetailResolver

class ResolversCartProductDetail(
    CartProductDetailResolver
):
    """Queries which can be performed by this  API"""

class MutationCreateCartProductDetail:
    create_cart_product_detail = CreateCartProductDetail.Field()