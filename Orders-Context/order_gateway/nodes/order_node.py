import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from order_ctx_database_sqlalchemy_14.models.order import ModelOrder


class OrderNode(SQLAlchemyObjectType):
    class Meta:
        model = ModelOrder
        interfaces = (graphene.relay.Node, )
