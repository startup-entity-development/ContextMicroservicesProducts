import graphene
from schemas.cart_product_detail_schema import ResolversCartProductDetail, MutationCreateCartProductDetail
from schemas.cart_schema import ResolversCart, MutationCart
from schemas.customer_schema import ResolversCustomer, MutationCustomer
from schemas.order_schema import ResolversOrder, MutationOrder
from schemas.order_status_schema import ResolversOrderStatus
from schemas.shopper_schema import ResolversShopper, MutationShopper

class QueryProtected(
    graphene.ObjectType,
    ResolversCartProductDetail,
    ResolversCart,
    ResolversCustomer,
    ResolversOrder,
    ResolversOrderStatus,
    ResolversShopper
    ):
    # node = graphene.relay.Node.Field()
    """Queries which can be performed by this  API"""

class MutationProtected(
    graphene.ObjectType,
    MutationShopper,
    MutationCustomer,
    MutationCart,
    MutationCreateCartProductDetail,
    MutationOrder
    ):
    # node = graphene.relay.Node.Field()
    """Queries which can be performed by this  API"""

schema_protected = graphene.Schema(query=QueryProtected, mutation=MutationProtected)