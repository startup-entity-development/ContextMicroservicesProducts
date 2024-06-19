import logging
import random
import sys
from typing import List
import uuid
from product_ctx_database_sqlalchemy_14.models.media_model import ModelMedia
from product_ctx_database_sqlalchemy_14.models.base import db_session   
from product_ctx_database_sqlalchemy_14.models.media_model import ModelMedia
from product_ctx_database_sqlalchemy_14.models.product_model import ModelProduct
from product_ctx_database_sqlalchemy_14.models.retailer_model import ModelRetailer
from product_ctx_database_sqlalchemy_14.models.sub_category_model import ModelSubCategory   
from product_ctx_database_sqlalchemy_14.models.category_model import ModelCategory  
from product_ctx_database_sqlalchemy_14.objects.category_object import CategoryDataBase
from product_ctx_database_sqlalchemy_14.objects.product_retailer import ProductRetailerAttributes, ProductRetailerDataBase
from product_ctx_database_sqlalchemy_14.objects.retailer_object import RetailerAttributes, RetailerDatabase
from product_ctx_database_sqlalchemy_14.objects.sub_category_object import SubCategoryDataBase 
from product_ctx_database_sqlalchemy_14.objects.product_object import ProductAttributes, ProductDatabase, UnitMeasure

# Load logging configuration
log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",)

def create_retailer():
    retailer = RetailerAttributes(name="retailer name",
                                  description="retailer description")
    retailer_db = RetailerDatabase(log)
    return retailer_db.create(retailer)

def create_product_retailer(id_product:int, id_retailer:int):
    
    product_retailer_attr = ProductRetailerAttributes(
        retailer_id=id_retailer,
        link_url=f"https://link_url_{id_product}",
        product_id=id_product,
        cost=random.uniform(1, 12.5),
        stock=random.randint(1, 100),
        increment_retailer=random.uniform(1, 12.5),
        is_in_stock=True,
        is_active=True)
    
    product_retailer_db = ProductRetailerDataBase(db_session=db_session, log=log)
    return product_retailer_db.create(product_retailer_attr)

def create_products( list_sub_categories:List[ModelSubCategory], product_db:ProductDatabase):
    list_product:List[ModelProduct] = []
    for i, sub_category in enumerate(list_sub_categories):
            print(f"sub_category: {sub_category.name}")
        
            for a in range(0, 10):
                api_id_product = uuid.uuid4()
                product_attr = ProductAttributes(
                    sub_category_id=sub_category.id,
                    api_id=f"{a} api_id - {api_id_product}",
                    name=f"n:{a} test product name",
                    title=f" {a} test product title {api_id_product}",
                    words_tags=f"{a} test product words tags",
                    brand=f"{a} test product brand",
                    base_increment=random.uniform(1, 12.5),
                    description=f"{a} test product description",
                    upc_barcode=None,
                    unit_measure= random.choice(list(UnitMeasure.__members__.values())).value,
                    weight=random.uniform(6, 24.4),
                    size="30x30x30",
                    unit_in_pack=None,
                    cost=random.uniform(1, 12.5),
                    dpci=f"{a} test product dpci",
                    tcin=random.randint(1000, 9999))
                
                product:ModelProduct = product_db.create(product=product_attr)  
                list_product.append(product)      
                print(f"product: {product.name}")        
        
    return list_product

def create_media(id_product:int, name:str=None, description:str=None , auto_commit:bool=True):
    """Create media model."""
    try:
        media = ModelMedia(
            product_id=id_product,
            name=f"media name: {name}",
            description=f"media description: {description}",
            link_url=f"https://target.scene7.com/is/image/Target/GUEST_795d2f12-0817-4faa-a9d1-96d8e6635046",
            is_main=True)
        
        db_session.add(media)
        if auto_commit: 
            db_session.commit()
        print(f"media: {media.name}")   
        log.info(f"create_media done")
    except Exception as e:
        log.error(f"file: setup_db.py method:, create_media fail {e}")



class MainTest():
    
    def __init__(self, log:logging.Logger):
        self.log = log
        self.log.info(f"TestCategory class called")
        self.number_categories_to_create:int = 1
        self.category_db = CategoryDataBase(db_session=db_session, log=self.log)
        self.subcategory_db = SubCategoryDataBase(db_session=db_session, log=self.log)        
        self.product_db = ProductDatabase(log=self.log)
        self.retailer_db = RetailerDatabase(log=self.log)
        self.product_retailer_db = ProductRetailerDataBase(db_session=db_session, log=self.log)
        
        
    def run_test_database(self):
        # create categories 
        list_categories:List[ModelCategory] = []
        list_sub_categories:List[ModelSubCategory] = [] 
        self.category_db.delete_all()
        # delete all in cascade .
        
        # create retailer
        retailer:ModelRetailer = create_retailer()
        
        
        for a in range(0, self.number_categories_to_create):
            api_id_category = uuid.uuid4()
            self.category_db.create(api_id=api_id_category,
                                    name=f"n:{a} test category name",
                                    description=f"{a} test category description",
                                    default_base_increment=random.uniform(1, 12.5))
        
        # get all categories
        list_categories=self.category_db.get_all()

        # create sub_categories
        for i, category in enumerate(list_categories):
            api_id_sub_category = uuid.uuid4()
            sub_category = self.subcategory_db.create(
                                                    api_id=api_id_sub_category,
                                                    id_category=category.id,
                                                    name=f"n:{i} test sub_category name",
                                                    description=f"{i} test sub_category description",
                                                    image=f"https://image_{i}.com",
                                                    default_base_increment=random.uniform(1, 12.5)
                                                    
                                                    )
            list_sub_categories.append(sub_category)
            self.log.info(f"sub_category: {sub_category.name}")
            
            list_product:List[ModelProduct] = create_products(list_sub_categories, self.product_db)
            for product in list_product:
                create_media(product.id, "product_media", product.description)
            
                create_product_retailer(product.id, retailer.id)
                
        self.log.info(f"-------------End of get and load list sub_categories -------------")
        
                
        self.log.info(f"-------------End of get and load list products ------------")
        
            
          
         
if __name__ == "__main__":
    log.info("Create models")
    main_test = MainTest(log)
    main_test.run_test_database()