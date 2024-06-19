from typing import List
import graphene
from graphql_relay import from_global_id
from product_ctx_database_sqlalchemy_14.models.product_model import ModelProduct
from product_ctx_database_sqlalchemy_14.objects.product_object import ProductDatabase
from mutations.resource_class import ClassFunctionsProduct, MediaGraphInput, ProductRetailerGraphInput, UpdateProductGraphInput
from nodes.product_media import Product
import logging


class UpdateProduct(graphene.Mutation):
    
    """Update a Product."""
    product = graphene.Field(lambda: Product, description="Product edited by this mutation.")

    class Arguments:
        product_input = UpdateProductGraphInput(required=True)
        media_input = graphene.List(MediaGraphInput, required=False)
        product_retailer_input = graphene.List(ProductRetailerGraphInput, required=False)

    
    def mutate(self, info, product_input, product_retailer_input=None, media_input=None):
        
        
        log = logging.getLogger(__name__)
        log.info(f"UpdateProduct Mutation: {product_input.get('upc_barcode')}")
        fuctionsProduct = ClassFunctionsProduct(log) 
        product_attributes  = fuctionsProduct.get_product_attributes(product_input)

        media_list = []
        product_retailer_list = []
        
        if media_input:
            media_list = fuctionsProduct.get_list_media_attributes(media_input)
        if product_retailer_input:
            product_retailer_list = fuctionsProduct.get_list_product_retailer_attributes(product_retailer_input)
    
        product_db:ProductDatabase = ProductDatabase(log)
        id_subcategory = int(from_global_id(product_attributes.sub_category_id).id)
        default_words_tags = fuctionsProduct.get_default_words_tags(product_attributes, id_subcategory)

        try:
            # Get the id of the subcategory
            product_attributes.sub_category_id = id_subcategory
            # Update the product and media
            product_attributes.api_id = f"manual_edited-{product_attributes.upc_barcode}"
            
            # Check if a least one retailer is active to set the product as active
            if fuctionsProduct.check_retailer_node_active(product_retailer_list):
                product_attributes.is_active = True
            else:
                product_attributes.is_active = False

            product_model:ModelProduct = product_db.update(
                                                product_attr=product_attributes,
                                                auto_commit=False,
                                                default_words_tags=default_words_tags)
                                              
            assert product_model.id is not None, "Product id is None after update product"

        except Exception as e:
            product_db.db_session.rollback()
            raise Exception(f"Error in UpdateProduct: {e}, error_code: $UPDATE0001")   
        
        if media_list:
            fuctionsProduct.recreate_media(product_id=product_model.id, media_list=media_list)
        if product_retailer_list:
            fuctionsProduct.recreate_product_retailer(product_id=product_model.id, product_retailer_list=product_retailer_list)
        
        product_db.db_session.commit()
        product_db.db_session.refresh(product_model)

        return UpdateProduct(product=product_model)

