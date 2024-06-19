import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from order_ctx_database_sqlalchemy_14.models.shopper import ModelShopper
from graphql_relay.node.node import from_global_id
from mutations.shopper_mutation import CreateShopper

class ShopperSchema(SQLAlchemyObjectType):
    class Meta:
        model = ModelShopper
        interfaces = (graphene.relay.Node,)
    
class ResolversShopper:
    # Shopper
    shopper_list = SQLAlchemyConnectionField(ShopperSchema.connection)
    get_shopper = graphene.Field(ShopperSchema, id=graphene.ID(required=True))

    def resolve_get_shopper(root, context, id):
        id_shopper = int(from_global_id(id).id)
        query = ShopperSchema.get_query(context)       
        shopper = query.filter(ModelShopper.id == id_shopper).first()
        return shopper

class MutationShopper:
    create_shopper = CreateShopper.Field()