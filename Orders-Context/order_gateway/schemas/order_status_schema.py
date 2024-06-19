import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from order_ctx_database_sqlalchemy_14.models.order_status import ModelOrderStatus
from graphql_relay.node.node import from_global_id

class OrderStatusSchema(SQLAlchemyObjectType):
    class Meta:
        model = ModelOrderStatus
        interfaces = (graphene.relay.Node,)
    
class ResolversOrderStatus:
    # OrderStatus
    order_status_list = SQLAlchemyConnectionField(OrderStatusSchema.connection)
    get_order_status = graphene.Field(OrderStatusSchema, id=graphene.ID(required=True))

    def resolve_get_order_status(root, context, id):
        id_order_status = int(from_global_id(id).id)
        query = OrderStatusSchema.get_query(context)       
        order_status = query.filter(ModelOrderStatus.id == id_order_status).first()
        return order_status
