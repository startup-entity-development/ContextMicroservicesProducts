import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from order_ctx_database_sqlalchemy_14.models.shopper import ModelShopper


class ShopperNode(SQLAlchemyObjectType):
    class Meta:
        model = ModelShopper
        interfaces = (graphene.relay.Node, )
