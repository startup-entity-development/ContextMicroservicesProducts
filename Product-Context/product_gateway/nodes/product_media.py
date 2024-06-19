import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql_relay import to_global_id
from product_ctx_database_sqlalchemy_14.models.media_model import ModelMedia
from product_ctx_database_sqlalchemy_14.models.product_model import ModelProduct
from product_ctx_database_sqlalchemy_14.models.product_retailer_model import ModelProductRetailer

def encodeBase64(id:int, name_id:str):
    if isinstance(id, int):
        return to_global_id(name_id, id)
    try:
        id_int = int(id)
        return to_global_id(name_id, id_int)
    except:
        return id

class Product(SQLAlchemyObjectType):
    sub_category_id = graphene.ID(description="SubCategory ID")

    class Meta:
        model = ModelProduct
        interfaces = (graphene.relay.Node, )
        
    def resolve_sub_category_id(self, info):
        return encodeBase64(self.sub_category_id, "SubCategoryId")
    
class Media(SQLAlchemyObjectType):
    class Meta:
        model = ModelMedia
        interfaces = (graphene.relay.Node, )

class ProductRetailer(SQLAlchemyObjectType):
    price = graphene.Float(description="Price of the Product")
    #convert retail_id (foreint key) integer to ID.graphene 
    retailer_id = graphene.ID(description="Retailer ID")
    product_id = graphene.ID(description="Product ID")
  
    class Meta:
        
        model = ModelProductRetailer
        interfaces = (graphene.relay.Node,)
        exclude_fields = ("cost")
        
    def resolve_retailer_id(self, info):
        return encodeBase64(self.retailer_id, "RetailerId")
    
    def resolve_product_id(self, info):
        return encodeBase64(self.product_id, "ProductId")
    
    
   
        
    def resolve_price(self, info):
        
        def calculate_price(product_increment, retailer_increment):
            if self.cost is not None and self.cost > 0:
                increment_product = (self.cost / 100) * product_increment
                increment_retailer = (self.cost / 100) * retailer_increment
                price =  self.cost + increment_product + increment_retailer
                if price > 0:
                    return round(price, 2)
            
            return 0.0 
            
        if self.id == "is_not_in_db":
            return 0.0     
        
        product_increment = self.product.base_increment
        if not product_increment:
            product_increment = self.product.SubCategory.default_base_increment
        if not product_increment:
            product_increment = self.product.SubCategory.Category.default_base_increment

        retailer_increment = self.increment_retailer
        
        if not product_increment :
            product_increment = 0
        if not retailer_increment:
            retailer_increment = 0

        return calculate_price(product_increment, retailer_increment)