from flask import request
import logging
import graphene
from order_ctx_database_sqlalchemy_14.objects.cart_object import CartDataBase, CartAttributesGateway
from resolvers.cart_resolver import CartSchema



class ObtainCart(graphene.Mutation):
    """Obtain Cart."""
    cart = graphene.Field(lambda: CartSchema, description="Cart created by this mutation.")
        
    def mutate(self, info):
        
        log = logging.getLogger(__name__)
        
        try:
            user_account_id = request.headers.get('X-Auth-Id')
            if not user_account_id:
                raise Exception('Invalid user account id')
        except Exception as e:
            raise Exception(f'Error in CartGraphInput: {e}')
        try:
            cart_input = {}
            cart_input["user_account_id"] = user_account_id
            cart_attributes = CartAttributesGateway().from_dict(cart_input)
        except Exception as e:
            raise Exception(f'Error in CartGraphInput: {e}')

        # Instantiate the cart database object
        cart_db:CartDataBase = CartDataBase(log)
        
        try:
            # Get user active cart, if not then create a new cart
            cart_model = cart_db.get_active_cart(user_account_id=cart_input["user_account_id"])
            if not cart_model:
                cart_model = cart_db.create(cart=cart_attributes, raise_integrety_except=True)
                cart_db.db_session.refresh(cart_model)

        except Exception as e:
            cart_db.db_session.rollback()
            raise Exception(f"Error in create cart: {e}")      
        
        
        return ObtainCart(cart=cart_model)
    