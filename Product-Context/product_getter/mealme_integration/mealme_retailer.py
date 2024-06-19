import logging
from typing import List

from product_ctx_database_sqlalchemy_14.models.retailer_model import ModelRetailer
from product_ctx_database_sqlalchemy_14.objects.retailer_object import RetailerDatabase
from product_ctx_database_sqlalchemy_14.models.base import db_session


class MealmeRetailer:
    
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.retailers_mealme:List[ModelRetailer] = []

    def get_retailers(self) -> List[ModelRetailer]:
        retailerDatabase = RetailerDatabase(log=self.log, db_session=db_session)
        retailers = retailerDatabase.get_by_api_name("mealme", only_active=False)
        self.retailers_mealme = retailers 
        return retailers
    
    def get_retailers_active(self) -> List[ModelRetailer]:
        retailerDatabase = RetailerDatabase(log=self.log, db_session=db_session)
        retailers = retailerDatabase.get_by_api_name("mealme", only_active=True)
        self.retailers_mealme = retailers
        return retailers

    
    
        