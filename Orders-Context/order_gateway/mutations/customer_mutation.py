import logging
import graphene
from order_ctx_database_sqlalchemy_14.objects.customer_object import CustomerDataBase, CustomerAttributesGateway
from nodes.customer_node import CustomerNode

class CustomerGraphAttribute:
    name = graphene.String(description= "Name of the Customer", required=True)
    stripe_customer_id = graphene.String(description= "Stripe id of the Customer", required=True)

class CustomerGraphInput(graphene.InputObjectType, CustomerGraphAttribute):
    """Arguments to create a Customer."""
    pass

class CreateCustomer(graphene.Mutation):
    """Create a Customer."""
    customer = graphene.Field(lambda: CustomerNode, description="Customer created by this mutation.")
    
    class Arguments:
        customer_input = CustomerGraphInput(required=True)
        
    def mutate(self, info, customer_input):
        
        log = logging.getLogger(__name__)
        
        try:
            customer_attributes = CustomerAttributesGateway().from_dict(customer_input)
        except Exception as e:
            raise Exception(f'Error in CustomerGraphInput: {e}')
        
        # Instantiate the customer database object
        customer_db:CustomerDataBase = CustomerDataBase(log)
        
        try:
            customer_model = customer_db.create(customer=customer_attributes, raise_integrety_except=True)
            customer_db.db_session.refresh(customer_model)
        except Exception as e:
            customer_db.db_session.rollback()
            if e.__class__.__name__ == "IntegrityError":
                raise Exception(f"Error in Create Customer: IntegrityError {e}")
            else:
                raise Exception(f"Error in Create Customer: {e}")        
        

        return CreateCustomer(customer=customer_model)
    