import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from order_ctx_database_sqlalchemy_14.models.customer import ModelCustomer


class CustomerNode(SQLAlchemyObjectType):
    class Meta:
        model = ModelCustomer
        interfaces = (graphene.relay.Node, )
