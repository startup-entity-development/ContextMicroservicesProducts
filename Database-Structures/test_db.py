import logging
import random
import sys
from typing import List
import uuid

from product_ctx_database_sqlalchemy_14.models.media_model import ModelMedia
from product_ctx_database_sqlalchemy_14.models.base import db_session   
from product_ctx_database_sqlalchemy_14.models.media_model import ModelMedia
from product_ctx_database_sqlalchemy_14.models.product_model import ModelProduct
from product_ctx_database_sqlalchemy_14.models.sub_category_model import ModelSubCategory   
from product_ctx_database_sqlalchemy_14.models.category_model import ModelCategory  
from product_ctx_database_sqlalchemy_14.objects.category_object import CategoryDataBase
from product_ctx_database_sqlalchemy_14.objects.sub_category_object import SubCategoryDataBase 
from product_ctx_database_sqlalchemy_14.objects.product_object import Product, ProductAttributes

# Load logging configuration
log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",)


def create_media(id_product:int, name:str=None, description:str=None , auto_commit:bool=True):
    """Create media model."""
    try:
        media = ModelMedia(
            product_id=id_product,
            name=f"media name: {name}",
            description=f"media description: {description}",
            url=f"url: {name}" )
        db_session.add(media)
        if auto_commit: 
            db_session.commit()
        print(f"media: {media.name}")   
        log.info(f"create_media done")
    except Exception as e:
        log.error(f"file: setup_db.py method:, create_media fail {e}")
        
class MainTest():
    
    def __init__(self, log:logging.Logger):
        super().__init__(log, db_session)
        self.log = log
        self.log.info(f"TestCategory class called")
        self.number_categories_to_create:int = 10
        self.category_db = CategoryDataBase(db_session=db_session, log=self.log)
        self.subcategory_db = SubCategoryDataBase(db_session,db_session, log=self.log)        

    def run_test_database(self):
        # create categories 
        list_categories:List[ModelCategory] = []
        list_sub_categories:List[ModelSubCategory] = [] 
        
        self.delete_all()
        
        for a in range(0, self.number_categories_to_create):
            api_id_category = uuid.uuid4()
            self.category_db.create(api_id=api_id_category ,name=f"n:{a} test category name", description=f"{a} test category description")
        
        # get all categories
        list_categories=self.category_db.get_all()
        
        
        # create sub_categories
        for i, category in enumerate(list_categories):
            api_id_sub_category = uuid.uuid4()
            sub_category = self.subcategory_db.create(api_id=api_id_sub_category,
                                                    id_category=category.id,
                                                    name=f"n:{i} test sub_category name",
                                                    description=f"{i} test sub_category description")
            list_sub_categories.append(sub_category)
            self.log.info(f"sub_category: {sub_category.name}")
            
        self.log.info(f"-------------End of get and load list sub_categories -------------")
        
        for i, sub_category in enumerate(list_sub_categories):
            print(f"sub_category: {sub_category.name}")
        
            for a in range(0, 10):
                api_id_product = uuid.uuid4()
                product_attr = ProductAttributes(
                    sub_category_id=sub_category.id,
                    api_id=f"{a} api_id - {api_id_product}",
                    name=f"n:{a} test product name", 
                    title=f"n:{a} test product title {api_id_product}",
                    description=f"{a} test product description", 
                    upc_barcode=f"{api_id_product} upc_barcode",
                    unit_measure="unit_measure",
                    size=f"{a} size",
                    link_url=f"{api_id_product} link_url",
                    cost=random.uniform(1.5, 75.5), 
                    dpci=f"{api_id_product} dpci"
                    )
                
                product:ModelProduct = self.create_product(product=product_attr)        
                print(f"product: {product.name}")        
                
        self.log.info(f"-------------End of get and load list products ------------")
        
        # delete categories
        for category in list_categories:
            self.log.info(f"delete category: {category.name}")
            self.delete(id_category=category.id)
            
          
         
if __name__ == "__main__":
    log.info("Create models")
    main_test = MainTest(log)
    main_test.run_test_database()