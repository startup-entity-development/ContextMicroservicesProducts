import logging
import time
from typing import Any, Dict, List, Tuple
from product_ctx_database_sqlalchemy_14.models.retailer_location_model import ModelRetailerLocation
from product_ctx_database_sqlalchemy_14.models.retailer_model import ModelRetailer
from product_ctx_database_sqlalchemy_14.objects.category_object import CategoryDataBase
from product_ctx_database_sqlalchemy_14.models.base import db_session
from product_ctx_database_sqlalchemy_14.objects.media_object import MediaAttributes, MediaDataBase
from product_ctx_database_sqlalchemy_14.objects.product_object import ProductAttributes, ProductDatabase, UnitMeasure
from product_ctx_database_sqlalchemy_14.objects.product_retailer import ProductRetailerAttributes, ProductRetailerDataBase
from product_ctx_database_sqlalchemy_14.objects.sub_category_object import SubCategoryDataBase
from product_ctx_database_sqlalchemy_14.objects.utils import is_alnum_or_space
from mealme_integration.api_object import ApiSources
from mealme_integration.mealme_data_classes import Category, Collector, MealmeArguments, Subcategory, Product
from mealme_integration.mealme_retailer import MealmeRetailer

class MealMe(ApiSources):

    def __init__(self, api_key:str="gilson:d27f945d-801d-4e4d-9cf6-e23c1ac2b576",
                    endpoint:str="https://api.mealme.ai"):
        
        self.log = logging.getLogger(__name__)
        self.log.info(f"RedCircle class called")
        self.endpoint_base = endpoint
        self.api_key = api_key
        self.mealmeRetailer = MealmeRetailer()
        self.retailers  = self.mealmeRetailer.get_retailers()
        self.categories:List[Category] = []
        self.collector:Collector
        self.db_session = db_session

        self.headers =  {
                "accept": "application/json",
                "Id-Token": self.api_key
                }

        super().__init__(api_key,self.log ,endpoint)
            

    def get_categories_retailer(self, retailer:ModelRetailer) -> List[Dict[str,Any]]:
        for retailer_location in retailer.location_retailer_edge:
            self.log.info(f"Retailer location {retailer_location.id}")
            self.get_categories_retailer_location(retailer.id_api, retailer.id, retailer_location)

    def get_categories_retailer_location(self,retailer_store_id:str, retailer_id_db:int, retailer_location:ModelRetailerLocation) -> Collector:
        self.log.info(f"Retailer location {retailer_location.id}")
        #url = "https://api.mealme.ai/details/inventory?store_id=fe0c0a68-5761-460e-b545-cf42ea05de07&pickup=false&include_quote=false&quote_preference=first_available&include_customizations=true&budget=20&user_latitude=37.7786357&user_longitude=-122.3918135&user_street_num=188&user_street_name=King%20Street&user_city=San%20Francisco&user_state=CA&user_zipcode=94107&user_country=US&image_height=300&image_width=300&available=true"

        params = {
            "store_id": retailer_store_id,
            "pickup": False,
            "include_quote": False,
            "user_latitude": retailer_location.latitude,
            "user_longitude": retailer_location.longitude,
            "user_street_num": 101,
            "user_street_name": retailer_location.street_addr,
            "user_city": retailer_location.city,
            "user_state": retailer_location.state,
            "user_zipcode": retailer_location.zipcode,
            "user_country": retailer_location.country,}
        
        data = self.get_dic_response(params=params, headers=self.headers, route="/details/inventory")
        
        mealme_arguments:MealmeArguments = MealmeArguments.from_dict(params)

        result = self.to_category(data["categories"])
        self.categories.extend(result)
        self.collector = Collector(categories=self.categories,
                            mealme_arguments=mealme_arguments,
                            id_retailer_db=retailer_id_db)

        return self.collector
         
    def get_all_categories(self, store_name:str) -> List[Dict[str,Any]]:
        retailer_selected = None
        for retailer in self.retailers:
            if retailer.name == store_name:
                retailer_selected = retailer
                break
        if not retailer_selected:
            raise Exception(f"Retailer {store_name} not found")
        self.get_categories_retailer(retailer_selected)

    def to_category(self, 
                     list_dict_categories:List[Dict[str,Any]],
                     ) -> List[Category] :
        
        result_list:List[Category] = []   
        
        for category in list_dict_categories:
            
            category_result = Category(
                name = category["name"],
                category_id = category["subcategory_id"],
                subcategories = [])
            
            result_list.append(category_result)

        return result_list

    def to_subcategory(self, 
                     list_dict_categories:List[Dict[str,Any]],
                     ) -> List[Subcategory] :

        result_list:List[Subcategory] = []   

        for subcategory in list_dict_categories:

            subcategory_result = Subcategory(
                name = subcategory["name"],
                subcategory_id = subcategory["subcategory_id"],
                products = [])
            
            result_list.append(subcategory_result)

        return result_list
    
    def get_subcategories(self, limit= None) -> Collector:
        if limit:
            categories_limited= self.collector.categories[:limit]
        else:
            categories_limited = self.collector.categories
        for category in categories_limited:
            params = self.collector.mealme_arguments.to_dict()
            params["subcategory_id"] = category.category_id
            time.sleep(1)
            data = self.get_dic_response(params=params, headers=self.headers, route="/details/inventory")
            result = self.to_subcategory(data["categories"])
            category.subcategories.extend(result)

        return self.collector
    
    def check_for_get_products(self,limit:int=None ) -> Collector:
        subcategories_to_remove = []
        total_subcategories = 0
        for category in self.collector.categories:
            for subcategory in category.subcategories:
                total_subcategories += 1
                params = self.collector.mealme_arguments.to_dict()
                params["subcategory_id"] = subcategory.subcategory_id
                time.sleep(0.5)
                data = self.get_dic_response(params=params, headers=self.headers, route="/details/inventory")
                result = data["categories"]
                if not result:
                    subcategories_to_remove.append(subcategory)
                    continue
                if result[0].get("menu_item_list"):
                    list_menu_item = result[0].get("menu_item_list")
                    self.to_product(list_menu_item, subcategory)
                else:
                    self.log.error(f"Error getting products: {result}")
                    raise Exception(f"Error getting products: {result}")
        
        self.log.warning(f"1 » total subcategories to check for products: {total_subcategories}")
        total_subcategories = 0
        for category in self.collector.categories:
            for subcategory in subcategories_to_remove:
                if subcategory in category.subcategories:
                    category.subcategories.remove(subcategory)
        for category in self.collector.categories:
            for subcategory in category.subcategories:
                total_subcategories += 1
        self.log.warning(f"2 » total subcategories to check for products: {total_subcategories}")


        return self.collector
    
    def to_product(self, 
                     menu_item_list:List[Dict[str,Any]],
                     subcategory:Subcategory    
                     ) -> None  :
                
        for product in menu_item_list:
            
            product_result = Product(
                name = product["name"],
                prince = product["price"],
                formatted_price = product["formatted_price"],
                is_available = product["is_available"],
                unit_size = product["unit_size"],
                unit_of_measurement = product["unit_of_measurement"],
                description = product["description"],
                image = product.get("image", None),
                product_id = product["product_id"])
            
            subcategory.products.append(product_result)

    def save_collection_in_file(self, name:str="") -> str:
        now = int(time.time())
        now_str = str(now)
        name_file = f"{now_str}_mealme_collector_{name}.json"
        self.collector.to_file(name_file)
        return now_str

    def collection_from_file(self,timestamp:str, name:str="") -> Collector:
        name_file = f"{timestamp}_mealme_collector_{name}.json"
        self.collector = Collector.from_file(name_file)
        return self.collector

    def is_category_in_db(self, category:Category,category_db: CategoryDataBase) -> int|None:
        """Check if category is in database."""
        id_api = category_db.create_id_api(category.name)
        category_model_db= category_db.get_by_id_api(id_api)
        if category_model_db:
            return category_model_db.id
        else:
            return None

    def is_subcategory_in_db(self, subcategory:Subcategory, subcategory_db:SubCategoryDataBase) -> int|None:
        """Check if subcategory is in database."""
        id_api = subcategory_db.create_id_api(subcategory.name)
        subcategory_model_db= subcategory_db.get_by_id_api(id_api)
        if subcategory_model_db:
            return subcategory_model_db.id
        else:
            return None
        
    def is_product_in_db(self, product:Product, product_db:ProductDatabase) -> int|None:
        """Check if product is in database."""
        length = len(product.image)
        image_product:str = product.image[length - 10:]
        id_api = ProductAttributes.create_id_api(f"{product.name} {product.get_dimensions_string()} {image_product}")
        product_model_db = product_db.get_by_api_id(id_api)
        if product_model_db:
            return product_model_db.id
        else:
            return None
        


    def get_words_tags(self, subcategory:Subcategory, category:Category) -> str:
        words_tags = f"{subcategory.name} {category.name}"
        words_tags = ''.join(e for e in words_tags if is_alnum_or_space(e))
        words_tags = ' '.join(words_tags.split())
        return words_tags
        
    def is_media_in_db(self,product:Product, media_db:MediaDataBase) -> int|None:
        """Check if media is in database."""
        media = media_db.get_by_product_id_and_url(product.id_db, product.image)
        if media:
            return media.id
        else:
            return None
        
    def is_product_retailer_in_db(self, product:Product, product_retailer_db:ProductRetailerDataBase) -> int|None:
        """
        Check if product_retailer is in database.
            self.collector.id_retailer_db
        """
        product_retailer = product_retailer_db.get_by_product_id_and_retailer_id(product.id_db, self.collector.id_retailer_db)
        if product_retailer:
            return product_retailer.id
        else:
            return None


    def save_category_in_db(self) -> None:
        category_db = CategoryDataBase(db_session=self.db_session, log=self.log)
        for category in self.collector.categories:
            if category.subcategories.__len__() == 0:
                self.log.warning(f"Category {category.name} has no subcategories")
                continue
            id_category = self.is_category_in_db(category, category_db )
            if not id_category:
                category_model_db = category_db.create(api_id=category.category_id,
                                   name=category.name,
                                   description="",
                                   default_base_increment=0.0)
                id_category = category_model_db.id
                category.id_db = id_category
                
            else:
                category.id_db = id_category
    
    def save_subcategory_in_db(self) -> None:
        for category in self.collector.categories:
            for subcategory in category.subcategories:
                if subcategory.products.__len__() == 0:
                    self.log.warning(f"Subcategory {subcategory.name} has no products")
                    continue
                subcategory_db = SubCategoryDataBase(db_session=self.db_session, log=self.log)
                id_sub_category = self.is_subcategory_in_db(subcategory, subcategory_db)
                if not id_sub_category:
                   category_model_db = subcategory_db.create(api_id=subcategory.subcategory_id,
                                          id_category=category.id_db,
                                          name=subcategory.name,
                                          description="",
                                          image=None,
                                          default_base_increment=None)
                   subcategory.id_db = category_model_db.id
                else:
                   subcategory.id_db = id_sub_category
    

    def save_products_in_db(self, force_update:bool=False) -> None:
        product_db = ProductDatabase(log=self.log)

        for category in self.collector.categories:
            for subcategory in category.subcategories:
                for product in subcategory.products:
                    if product.image is None or len(product.image) > 350 :
                        self.log.warning(f"Product {product.name} has no image or is not valid")
                        continue

                    id_product = self.is_product_in_db(product, product_db)
                    
                    if id_product and not force_update:
                        product.id_db = id_product
                        continue

                    unit_m, size, weight = product.get_product_dimensions()
                    words_tags = self.get_words_tags(subcategory, category)
                    length = len(product.image)
                    image_product:str = product.image[length - 10:]

                    productAttributes= ProductAttributes(
                        sub_category_id=subcategory.id_db,
                        title=product.name,
                        brand="",
                        base_increment=None,
                        words_tags=words_tags,
                        api_id=ProductAttributes.create_id_api(f"{product.name} {product.get_dimensions_string()} {image_product}"),
                        description=product.description,
                        upc_barcode=None,
                        name=product.name,
                        unit_measure=unit_m,
                        weight=weight,  
                        size=size
                    )

                    if not id_product:
                        product_model_db = product_db.create(productAttributes, raise_integrity_except=True)
                        product.id_db = product_model_db.id
                    
                    elif force_update:
                        productAttributes.id = id_product
                        product_db.update(productAttributes)
                        product.id_db = id_product
    
    def save_media_product(self, force_update:bool= False):
        media_db = MediaDataBase(log=self.log)
        for category in self.collector.categories:
            for subcategory in category.subcategories:
                for product in subcategory.products:
                    if product.image is None or len(product.image) > 350 :
                        self.log.warning(f"Product {product.name} has no image or is not valid")
                        continue
                    id_media = self.is_media_in_db(product,media_db)
                    media = MediaAttributes(
                            product_id=product.id_db,
                            media_type="image",
                            link_url=product.image,
                            is_main=True,
                            name=product.name[:50],
                            description=product.description[:255]
                        )
                    if not id_media:
                        media_model_db = media_db.create(media)
                        product.id_media_db = media_model_db.id
                    elif force_update:
                        media.id = id_media
                        media_db.update(media)
                        product.id_media_db = id_media
                    else:
                        product.id_media_db = id_media
    
    def save_product_retailer(self, force_update:bool= False):
        product_retailer_db = ProductRetailerDataBase(log=self.log)
        for category in self.collector.categories:
            for subcategory in category.subcategories:
                for product in subcategory.products:
                    if product.image is None or  len(product.image) > 350 :
                        self.log.warning(f"Product {product.name} has no image or is not valid")
                        continue
                    id_product_retailer = self.is_product_retailer_in_db(product,product_retailer_db)
                    price:float = float(product.formatted_price.replace("$",""))
                    productRetailerAttributes= ProductRetailerAttributes(
                        product_id=product.id_db,
                        retailer_id=self.collector.id_retailer_db,
                        cost=price,
                        increment_retailer=0.0,
                        stock=1,
                        is_active=True,
                        is_in_stock=True,
                        link_url=None
                    )
                    if not id_product_retailer:
                        product_retailer_model_db = product_retailer_db.create(productRetailerAttributes)
                        product.id_retailer_db = product_retailer_model_db.id
                    elif force_update:
                        productRetailerAttributes.id = id_product_retailer
                        product_retailer_db.update(productRetailerAttributes)
                        product.id_retailer_db = id_product_retailer
                    else:
                        product.id_retailer_db = id_product_retailer
                    
                    
        
    

        
                    
                    
                    

                    
                    
                    


            
    
        
    



                
                        
        
