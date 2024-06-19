import logging
from typing import List
from mealme_integration.mealme_object import MealMe
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
        self.mealme = MealMe()

    def create_collection(self, store_name:str="store_name") -> str:
        self.mealme.get_all_categories(store_name=store_name)
        self.mealme.get_subcategories()
        self.mealme.check_for_get_products()
        return self.mealme.save_collection_in_file(name=store_name)

    def load_in_data_base(self, store_name:str="store_name", timestamp:str="0"):
        self.mealme.collection_from_file(timestamp=timestamp, name=store_name)
        self.mealme.save_category_in_db()
        self.mealme.save_subcategory_in_db()
        self.mealme.save_products_in_db(force_update=False)
        self.mealme.save_media_product()
        self.mealme.save_product_retailer()


if __name__ == "__main__":
    populate_database = PopulateDatabase()
    LIST_STORE_NAME = ["Total Wine",]

    for STORE_NAME in LIST_STORE_NAME:
        str_timestamp = populate_database.create_collection(store_name=STORE_NAME)
        populate_database.load_in_data_base(store_name=STORE_NAME, timestamp=str_timestamp)

    #populate_database.load_in_data_base(store_name="CVS Pharmacy", timestamp="1710764652")