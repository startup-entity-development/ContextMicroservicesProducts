import graphene
from schemas.schema_product import MutationProduct
from schemas.schema_category import ResolversCategory, ResolversSubCategory
from schemas.schema_product import MutationProduct, ResolversProduct
from schemas.schema_retailer import ResolversRetailer

class QueryProtected(graphene.ObjectType,
                     ResolversCategory,
                     ResolversSubCategory,
                     ResolversProduct,
                     ResolversRetailer):
    
    # node = graphene.relay.Node.Field()
    """Queries which can be performed by this  API"""




class MutationProtected(graphene.ObjectType, MutationProduct):
    
    # node = graphene.relay.Node.Field()
    """Queries which can be performed by this  API"""


schema_protected = graphene.Schema(query=QueryProtected, mutation=MutationProtected)