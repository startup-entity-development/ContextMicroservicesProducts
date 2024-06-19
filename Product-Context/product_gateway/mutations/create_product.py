import logging
from typing import Dict, List
import graphene
from graphql_relay import from_global_id
from product_ctx_database_sqlalchemy_14.models.product_model import ModelProduct
from product_ctx_database_sqlalchemy_14.models.sub_category_model import ModelSubCategory
from product_ctx_database_sqlalchemy_14.objects.product_object import ProductDatabase
from product_ctx_database_sqlalchemy_14.objects.media_object import  MediaDataBase
from product_ctx_database_sqlalchemy_14.objects.product_retailer import ProductRetailerDataBase
from product_ctx_database_sqlalchemy_14.objects.sub_category_object import SubCategoryDataBase
from mutations.resource_class import ClassFunctionsProduct, ProductGraphInput, MediaGraphInput, ProductRetailerGraphInput
from nodes.product_media import Product


class CreateProduct(graphene.Mutation):
    
    """Create a Product."""
    product = graphene.Field(lambda: Product, description="Product createdcd  by this mutation.")

    class Arguments:
        product_input = ProductGraphInput(required=True)
        media_input = graphene.List(MediaGraphInput, required=True)
        product_retailer_input = graphene.List(ProductRetailerGraphInput, required=True)

    
    def mutate(self, info, product_input, product_retailer_input, media_input):
        
        
        log = logging.getLogger(__name__)
        log.info(f"CreateProduct Mutation: {product_input.get('upc_barcode')}")
        fuctionsProduct = ClassFunctionsProduct(log) 
        product_attributes  = fuctionsProduct.get_product_attributes(product_input)
        product_retailer_list = fuctionsProduct.get_list_product_retailer_attributes(product_retailer_input)
        media_list = fuctionsProduct.get_list_media_attributes(media_input)
        
        
        product_db:ProductDatabase = ProductDatabase(log)
        id_subcategory = int(from_global_id(product_attributes.sub_category_id).id)

        default_words_tags = fuctionsProduct.get_default_words_tags(product_attributes, id_subcategory)

        try:
            # Get the id of the subcategory
            product_attributes.sub_category_id = id_subcategory
            # Create the product and media
            product_attributes.api_id = f"manual_created-{product_attributes.upc_barcode}"
            
            # Check if a least one retailer is active to set the product as active
            if fuctionsProduct.check_retailer_node_active(product_retailer_list):
                product_attributes.is_active = True
            else:
                product_attributes.is_active = False
            
            product_model:ModelProduct = product_db.create(product_attr=product_attributes,
                                                auto_commit=False,
                                              raise_integrity_except=True,
                                                default_words_tags= default_words_tags)
                                              
            assert product_model.id is not None, "Product id is None after create product"

        except Exception as e:
            product_db.db_session.rollback()
            if e.__class__.__name__ == "IntegrityError":
                if e.orig.pgerror.find("Product_api_id_key") != -1:
                    raise Exception(f"Product already exists, upc_barcode: {product_attributes.upc_barcode}, error_code: $RPBUNIDB001")
                else:
                    raise Exception(f"Error in CreateProduct: IntegrityError {e}, error_code: $RPBUNIDB002")
            else:
                raise Exception(f"Error in CreateProduct: {e}, error_code: $RPBUNIDB003")        
        
        fuctionsProduct.create_media(product_id=product_model.id, media_list=media_list)
        fuctionsProduct.creare_product_retailer(product_id=product_model.id, product_retailer_list=product_retailer_list)
        product_db.db_session.commit()
        product_db.db_session.refresh(product_model)
  
        return CreateProduct(product=product_model)
