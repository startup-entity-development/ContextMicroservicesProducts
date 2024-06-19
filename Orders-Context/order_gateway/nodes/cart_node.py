import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from order_ctx_database_sqlalchemy_14.models.cart import ModelCart


class CartNode(SQLAlchemyObjectType):
    class Meta:
        model = ModelCart
        interfaces = (graphene.relay.Node, )
