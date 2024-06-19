import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from order_ctx_database_sqlalchemy_14.models.customer import ModelCustomer
from graphql_relay.node.node import from_global_id
from mutations.customer_mutation import CreateCustomer

class CustomerSchema(SQLAlchemyObjectType):
    class Meta:
        model = ModelCustomer
        interfaces = (graphene.relay.Node,)
    
class ResolversCustomer:
    # Customer
    customer_list = SQLAlchemyConnectionField(CustomerSchema.connection)
    get_customer = graphene.Field(CustomerSchema, id=graphene.ID(required=True))

    def resolve_get_customer(root, context, id):
        id_customer = int(from_global_id(id).id)
        query = CustomerSchema.get_query(context)       
        customer = query.filter(ModelCustomer.id == id_customer).first()
        return customer
    
class MutationCustomer:
    create_customer = CreateCustomer.Field()
