import logging
import graphene
from graphql_relay import from_global_id
from order_ctx_database_sqlalchemy_14.objects.cart_product_detail_object import CartProductDetailDataBase, CartProductDetailAttributesGateway
from nodes.cart_detail_product_node import CartProductDetailNode
from resolvers.cart_resolver import CartSchema
from services.product_service import resolve_getProductById

class CartProductDetailGraphAttribute:
    quantity = graphene.Int(description= "Quantity of the cart item", required=True)
    cart_id = graphene.ID(description= "Cart id of the cart item", required=True)
    product_id = graphene.ID(description= "Product id of the cart item", required=True)
    retailer_id = graphene.ID(description= "Retailer id of the cart item", default_value="UmV0YWlsZXJJZDoy")
    preference_product = graphene.String(description= "Preference of the cart item", default_value="", required=False)

    
class CartProductDetailGraphInput(graphene.InputObjectType, CartProductDetailGraphAttribute):
    """Arguments to create a Cart item."""
    pass

class CreateCartProductDetail(graphene.Mutation):
    """Create a Cart item."""
    cart = graphene.Field(lambda: CartSchema, description="Cart item created by this mutation.")
    
    class Arguments:
        input = CartProductDetailGraphInput(required=True)
        
    def mutate(self, info, input):
        
        log = logging.getLogger(__name__)
        product_detail = None
        try:
            product_detail = resolve_getProductById(input.product_id)
        except Exception as e:
            raise Exception(f'Error in CartItemGraphInput: {e}')
            
        if not product_detail or not "id" in product_detail:
            raise Exception(f'Product not exists')
        try:
            input["cart_id"] = int(from_global_id(input.cart_id).id)
            input["product_id"] = int(from_global_id(product_detail["id"]).id)
        except Exception as e:
            raise Exception(f'Error in CartItemGraphInput: {e}')
        
        # Instantiate the cart item database object
        cart_product_detail_db:CartProductDetailDataBase = CartProductDetailDataBase(log)
        try:
            cart_product_detail_model = cart_product_detail_db.get_by_cart_and_product(
                input["cart_id"],
                input["product_id"]
            )
            id_retailer = int(from_global_id(input.retailer_id).id)
            list_node_retailer = product_detail["retailerEdge"]["edges"]
            retailer_dict = next((retailer for retailer in list_node_retailer if  int(from_global_id(retailer["node"]["retailerId"]).id)  == id_retailer), None)
            
            if not retailer_dict:
                raise Exception(f"Retailer not found")
            
            input["price"] = retailer_dict["node"]["price"]
            input["retailer_id"] = id_retailer
            input["retailer_name"] = retailer_dict["node"]["retailer"]["name"]
            cart_product_detail_attributes = CartProductDetailAttributesGateway().from_dict(input)

            if not cart_product_detail_model:
                cart_product_detail_model = cart_product_detail_db.create(cart_product_detail=cart_product_detail_attributes, raise_integrety_except=True)
                cart_product_detail_db.db_session.refresh(cart_product_detail_model)
            else:
                cart_product_detail_model = cart_product_detail_db.update(cart_product_detail_id=cart_product_detail_model.id,
                                                                           cart_product_detail=cart_product_detail_attributes, 
                                                                           raise_integrety_except=True)

        except Exception as e:
            cart_product_detail_db.db_session.rollback()
            raise Exception(f"Error in create cart item: {e}")      
        
        cart: CartSchema = CartSchema.get_query(info).get(input["cart_id"])

        return CreateCartProductDetail(cart=cart)
    