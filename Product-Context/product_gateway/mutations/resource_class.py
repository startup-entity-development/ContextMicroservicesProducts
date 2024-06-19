from typing import Dict, List
import graphene
from product_ctx_database_sqlalchemy_14.models.sub_category_model import ModelSubCategory
from product_ctx_database_sqlalchemy_14.objects.media_object import MediaAttributes, MediaDataBase
from product_ctx_database_sqlalchemy_14.objects.product_object import ProductAttributes
from product_ctx_database_sqlalchemy_14.objects.product_retailer import ProductRetailerAttributes, ProductRetailerDataBase
from product_ctx_database_sqlalchemy_14.objects.sub_category_object import SubCategoryDataBase
from product_ctx_database_sqlalchemy_14.models.base import db_session


class UnitOfMeasure(graphene.Enum):
    ounce = "ounce"
    pound = "pound"
    kilo = "kilo"
    gram = "gram"
    liter = "liter"
    gallon = "gallon"
    milliliter = "milliliter"

class ClassFunctionsProduct:

    def __init__(self, log):
        self.log = log
        self.media_db = MediaDataBase(log)
        self.product_retailer_db = ProductRetailerDataBase(log)
        self.log.info("ClassFunctionsProduct")

    def get_product_attributes(self, product_input) -> ProductAttributes:
        product_attributes = None
        self.log.info(f"get_product_attributes: {product_input}")
        try:
            product_attributes = ProductAttributes.from_dict(obj_dict=product_input)
        except Exception as e:
            raise Exception(f'Error in ProductGraphInput: {e}')
        return product_attributes

    def get_list_media_attributes(self, media_input:List[Dict]) -> List[MediaAttributes]:
        media_attributes = None
        list_media_attributes = []
        self.log.info(f"get_list_media_attributes: {media_input}")
        try:
            for media in media_input:
                if media.get('product_id') is None:
                    media['product_id'] = None
                media_attributes = MediaAttributes.from_dict(media)
                list_media_attributes.append(media_attributes)
        except Exception as e:
            raise Exception(f'Error in MediaGraphInput: {e}')
        return list_media_attributes
    
    def get_list_product_retailer_attributes(self, product_retailer_input:Dict) -> List[ProductRetailerAttributes]:
        product_retailer_attributes = None
        list_product_retailer_attributes = []
        self.log.info(f"get_list_product_retailer_attributes: {product_retailer_input}")
        try:
            for product_retailer in product_retailer_input:
                if product_retailer.get('product_id') is None:
                    product_retailer['product_id'] = None
                product_retailer_attributes = ProductRetailerAttributes.from_dict(product_retailer)
                list_product_retailer_attributes.append(product_retailer_attributes)
        except Exception as e:
            raise Exception(f'Error in ProductRetailerGraphInput: {e}')
        return list_product_retailer_attributes

    def check_retailer_node_active(self, list_product_retailer_attr:List[ProductRetailerAttributes]) -> bool:
        for product_retailer in list_product_retailer_attr:
            if  product_retailer.is_active:
                return True
        return False
    
    def get_default_words_tags(self, product_attributes:ProductAttributes, id_subcategory:int)->str:
        try:
            default_words_tags = product_attributes.words_tags    
            if default_words_tags is None:
                subcategory_db = SubCategoryDataBase(db_session=db_session, log=self.log)
                subcategory:ModelSubCategory = subcategory_db.get(id=id_subcategory)
                default_words_tags =subcategory.name
                if default_words_tags is None:
                    default_words_tags = ""
        except Exception as e:
            raise Exception(f'Error in get default_words_tags: {e}')
        return default_words_tags    
        
    def recreate_media(self, product_id:int, media_list:List[MediaAttributes] )->None:
        """Reacreate the media of the product."""
        
        try: 
            self.delete_media(product_id)
            self.create_media(product_id, media_list)
        except Exception as e:
            self.media_db.db_session.rollback()
            raise Exception(f'Error in Recreate media {e}')
    

    def delete_media(self, product_id:int,)->None:
        """Delete the media of the product."""

        try: 
            self.media_db.delete_by_product_id(
                    product_id=product_id,
                    auto_commit=False,
                )
        except Exception as e:
            self.media_db.db_session.rollback()
            raise Exception(f'Error in DeleteMedia: {e}')
    
    def create_media(self, product_id:int, media_list:List[MediaAttributes])->None:
        """Update the media of the product."""
        try:
            for media in media_list:
                media.product_id = product_id
                self.media_db.create(media, auto_commit=False)
        except Exception as e:
            self.media_db.db_session.rollback()
            raise Exception(f'Error in CreateMedia: {e}')
    
    
    def recreate_product_retailer(self, product_id:int, product_retailer_list:List[ProductRetailerAttributes] )->None:
        """Reacreate the product retailer of the product."""
        
        try: 
            self.delete_product_retailer(product_id)
            self.creare_product_retailer(product_id, product_retailer_list)
        except Exception as e:
            self.product_retailer_db.db_session.rollback()
            raise Exception(f'Error in RecreateProductRetailer: {e}')
    
    def delete_product_retailer(self, product_id:int,)->None:
        """Delete the product retailer of the product."""

        try: 
            self.product_retailer_db.delete_by_product_id(
                    product_id=product_id,
                    auto_commit=False,
                )
        except Exception as e:
            self.product_retailer_db.db_session.rollback()
            raise Exception(f'Error in DeleteProductRetailer: {e}')
        
    def creare_product_retailer(self, product_id:int, product_retailer_list:List[ProductRetailerAttributes] )->None:
        try:
            for product_retailer in product_retailer_list:
                product_retailer.product_id = product_id
                self.product_retailer_db.create(product_retailer, auto_commit=False)
        except Exception as e:
            self.product_retailer_db.db_session.rollback()
            raise Exception(f'Error in UpdateProductRetailer: {e}')
        
    


class ProductGraphAttribute:
    """
    Remove the cost and retailer from ProductGraphAttribute field

    """
    upc_barcode = graphene.String(description= "UpcBarcode of the Product.", required=True)
    sub_category_id = graphene.ID(description= "Id of the SubCategory", required=True)
    title = graphene.String(description= "Title of the Product", required=True)
    size = graphene.String(description= "Size of the Product", required=True)
    brand = graphene.String(description= "Brand of the Product", required=True)
    description = graphene.String(description= "Description of the Product", required=True)

    #new optionas fields product
    words_tags = graphene.String(description= "TagsWords of the Product", required=False, default_value=None)
    weight = graphene.Float(description= "Weight of the Product", required=False, default_value=None)
    unit_measure = UnitOfMeasure(description= "Unit of Measure of the Product", required=False, default_value=None)
    base_increment = graphene.Float(description= "Product Base Increment of the Product", required=False, default_value=None)
    unit_in_pack = graphene.Int(description= "Unit in Pack of the Product", required=False, default_value=None)
    is_active = graphene.Boolean(description= "Status of the Product", required=False, default_value=True)

class UpdateProductGraphAttribute(ProductGraphAttribute):
    id = graphene.ID(description= "Id of the Product", required=True)

class ProductRetailerGraphAttribute:
    retailer_id = graphene.ID(description= "Id of the Retailer", required=True)
    cost = graphene.Float(description= "Cost of the Product", required=True)    
    increment_retailer = graphene.Float(description= "Increment based in the retailer", required=False, default_value=1)
    stock = graphene.Int(description= "Stock of the Product", required=False, default_value=None)
    is_active = graphene.Boolean(description= "Status of the Product", required=False, default_value=True)
    is_in_stock = graphene.Boolean(description= "Status of the Product", required=False, default_value=True)

class MediaGraphAttribute:
    link_url = graphene.String(description= "Image Url of the Product", required=True)
    is_main = graphene.Boolean(description= "Is Main Image of the Product", required=False)
    media_type = graphene.String(description= "Media Type of the Product", required=True)
    name = graphene.String(description= "Name of the Product", required=False)

class ProductGraphInput(graphene.InputObjectType, ProductGraphAttribute):
    """Arguments to create a Product."""
    pass

class UpdateProductGraphInput(graphene.InputObjectType, UpdateProductGraphAttribute):
    """Arguments to create a Product."""
    pass

class MediaGraphInput(graphene.InputObjectType, MediaGraphAttribute):
    """Arguments to create a Media."""
    pass

class ProductRetailerGraphInput(graphene.InputObjectType, ProductRetailerGraphAttribute):
    """Arguments to create a ProductRetailer."""
    pass

