import graphene
from schemas.schema_category import ResolversCategory, ResolversSubCategory
from schemas.schema_product import ResolversProduct
from schemas.schema_retailer import ResolversRetailerPublic

class QueryPublic(graphene.ObjectType,
                   ResolversCategory,
                     ResolversSubCategory,
                       ResolversProduct,
                       ResolversRetailerPublic
                       ):
    
    # node = graphene.relay.Node.Field()
    """Queries which can be performed by this  API"""


schema_public = graphene.Schema(query=QueryPublic)





