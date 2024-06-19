import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from order_ctx_database_sqlalchemy_14.models.cart_product_detail import ModelCartProductDetail


class CartProductDetailNode(SQLAlchemyObjectType):
    class Meta:
        model = ModelCartProductDetail
        interfaces = (graphene.relay.Node, )
