import logging
import graphene
from graphql_relay import from_global_id
from order_ctx_database_sqlalchemy_14.objects.shopper_object import ShopperDataBase, ShopperAttributesGateway
from nodes.shopper_node import ShopperNode

class ShopperGraphAttribute:
    name = graphene.String(description= "Name of the Shopper", required=True)

class ShopperGraphInput(graphene.InputObjectType, ShopperGraphAttribute):
    """Arguments to create a Shopper."""
    pass

class CreateShopper(graphene.Mutation):
    """Create a Shopper."""
    shopper = graphene.Field(lambda: ShopperNode, description="Shopper created by this mutation.")
    
    class Arguments:
        shopper_input = ShopperGraphInput(required=True)
        
    def mutate(self, info, shopper_input):
        
        log = logging.getLogger(__name__)
        
        try:
            shopper_attributes = ShopperAttributesGateway().from_dict(shopper_input)
        except Exception as e:
            raise Exception(f'Error in ShopperGraphInput: {e}')
        
        # Instantiate the shopper database object
        shopper_db:ShopperDataBase = ShopperDataBase(log)
        
        try:
            shopper_model = shopper_db.create(shopper=shopper_attributes, raise_integrety_except=True)
            shopper_db.db_session.refresh(shopper_model)
        except Exception as e:
            shopper_db.db_session.rollback()
            raise Exception(f"Error in create shopper: {e}")      
        
        
        return CreateShopper(shopper=shopper_model)
    