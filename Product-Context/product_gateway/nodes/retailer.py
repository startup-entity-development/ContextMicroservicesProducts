
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from product_ctx_database_sqlalchemy_14.models.retailer_model import ModelRetailer


class Retailer(SQLAlchemyObjectType):

    class Meta:
        model = ModelRetailer
        interfaces = (graphene.relay.Node,)