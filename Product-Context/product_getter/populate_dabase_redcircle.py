import logging
from typing import List
from redcircle_integration.category_redcircle import CategoryRedCircle
from redcircle_integration.product_redcircle import ProductRedCircle
from redcircle_integration.sub_category_redcircle import SubCategoryRedCircle
from product_ctx_database_sqlalchemy_14.models.base  import db_session
from product_ctx_database_sqlalchemy_14.models.category_model import ModelCategory
from product_ctx_database_sqlalchemy_14.objects.category_object import CategoryDataBase
from product_ctx_database_sqlalchemy_14.objects.sub_category_object import SubCategoryDataBase


class PopulateDatabase():
    
    def __init__(self) -> None:
        super().__init__()
        self.log = logging.getLogger(__name__)
        self.log.info(f"PopulateDatabase class called")
        self.db_session = db_session
        self.category_db:CategoryDataBase=CategoryDataBase(db_session=self.db_session, log=self.log)
        self.sub_category_db:SubCategoryDataBase=SubCategoryDataBase(db_session=self.db_session, log=self.log)
        self.category_red_circle:CategoryRedCircle=CategoryRedCircle(object_database=self.category_db)
        self.subcategory_red_circle:SubCategoryRedCircle=SubCategoryRedCircle(object_database=self.sub_category_db)
        self.product_red_circle:ProductRedCircle=ProductRedCircle(category_red_circle=self.category_red_circle,
                                                                  subcategory_red_circle=self.subcategory_red_circle)

    def load_all_categories(self,):
        self.category_red_circle.save_in_db()

    def load_all_subcategories(self) -> None:
        list_categories:List[ModelCategory] = self.category_db.get_all()
        for category_in_db in list_categories:
            self.subcategory_red_circle.update_database(id_api_category=category_in_db.api_id,
                                                        id_category=category_in_db.id)

    def load_all_products(self) -> None:
        self.product_red_circle.update_database_from_request(start=0, to=15)
        self.product_red_circle.create_success_sub_category_product_from_file_json()

    def create_collection_file_subcategories(self) -> None:
        self.subcategory_red_circle.create_categories_cvs_file_bunch_request()
    
    def create_collection_file_products(self) -> None:
        self.product_red_circle.create_products_cvs_file_bunch_request()
        

    def get_initial_pagination(self) -> None:
        self.product_red_circle.create_initial_pagination(list_product_search_result=
                                                          self.product_red_circle.list_product_search_result)
    
    
    def load_products_collection(self) -> None:
        self.product_red_circle.load_product_from_json_file()
    
    def update_product_description_and_barcode(self) -> None:
        self.product_red_circle.update_product_details_from_file_json()
        
        

if __name__ == "__main__":
    populate_database = PopulateDatabase()
    #populate_database.create_collection_file_products()
    #populate_database.create_collection_file_subcategories()
    
    #populate_database.load_all_categories()
    #populate_database.load_all_subcategories()
    
    #populate_database.load_products_collection()
    #populate_database.update_product_description_and_barcode()

    # for i in range(0, 2):
    #     populate_database.load_all_products()
    # print("------------------------------------")
    # print("Populate database with products done")
    #populate_database.load_all_products()