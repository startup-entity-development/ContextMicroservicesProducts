from flask import request
import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from order_ctx_database_sqlalchemy_14.models.cart_product_detail import ModelCartProductDetail
from order_ctx_database_sqlalchemy_14.models.order import ModelOrder
from resolvers.cart_product_detail_resolver import ProductSchema
from resolvers.cart_resolver import CartSchema
from graphql_relay.node.node import from_global_id, to_global_id

class OrderSchema(SQLAlchemyObjectType):
    cart = graphene.Field(CartSchema)
    class Meta:
        model = ModelOrder
        interfaces = (graphene.relay.Node,)

    def resolve_cart(self, info):
        return self.cart
    
class OrderResolver:
    # Order
    order_list = SQLAlchemyConnectionField(OrderSchema.connection)
    get_order = graphene.Field(OrderSchema, id=graphene.ID(required=True))
    orders_account = SQLAlchemyConnectionField(OrderSchema)

    def resolve_get_product(root, context, id):
        order_id = int(from_global_id(id).id)
        query = OrderSchema.get_query(context)       
        order = query.filter(ModelOrder.id == order_id).first()

        return order
    
    
    def resolve_orders_account(root, context):
        query = OrderSchema.get_query(context)    
        user_account_id = int(request.headers.get('X-Auth-Id'))   
        orders = query\
            .filter_by(user_account_id = user_account_id)\
            .order_by(ModelOrder.id.desc())\
            .limit(10)\
            .offset(0).all()
        
        return orders
    
    