from dataclasses import dataclass
from typing import Any, List

from product_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase
from product_ctx_database_sqlalchemy_14.models.base import db_session
from product_ctx_database_sqlalchemy_14.models.product_retailer_model import ModelProductRetailer

@dataclass
class ProductRetailerAttributes(): 
    retailer_id:int
    product_id:int
    link_url:str
    cost:float
    increment_retailer:float
    stock:int
    is_active:bool
    is_in_stock:bool
    
    @property
    def model_dictionary(self) ->dict:
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelProductRetailer.__dict__.keys()
        }


class ProductRetailerDataBase(ObjectDataBase):
    
    def __init(self,log):
        self.log = log
        self.db_session = db_session
        super().__init__(self.db_session, self.log)
    
    def create(self, product_retailer_attributes:ProductRetailerAttributes, auto_commit = True)->ModelProductRetailer:
        try:
            product_retailer_model:ModelProductRetailer = ModelProductRetailer(**product_retailer_attributes.model_dictionary)
            self.db_session.add(product_retailer_model)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.db_session.refresh(product_retailer_model)
            return product_retailer_model
        except Exception as e:
            self.log.error(f"Error creating product retailer: {e}")
            raise Exception(f"Error creating product retailer: {e}")
        
    def get(self, product_retailer_id:int)->ModelProductRetailer:
        try:
            product_retailer = self.db_session.query(ModelProductRetailer).filter(ModelProductRetailer.id == product_retailer_id).first()
        except Exception as e:
            self.log.error(f"Error getting product retailer: {e}")
            raise Exception(f"Error getting product retailer: {e}")
        
        return product_retailer
    
    def delete_all(self, auto_commit:bool = True)->None:
        try:
            self.db_session.query(ModelProductRetailer).delete()
            if auto_commit:
                self.db_session.commit()
        except Exception as e:
            self.log.error(f"Error deleting all product retailers: {e}")
            raise Exception(f"Error deleting all product retailers: {e}")
        
    def delete(self, product_retailer_id:int, auto_commit:bool = True)->None:
        try:
            product_retailer = self.db_session.query(ModelProductRetailer).filter(ModelProductRetailer.id == product_retailer_id).first()
            self.db_session.delete(product_retailer)
            if auto_commit:
                self.db_session.commit()
        except Exception as e:
            self.log.error(f"Error deleting product retailer: {e}")
            raise Exception(f"Error deleting product retailer: {e}")
        
    def get_all(self) -> List[Any]:
        try:
            product_retailers = self.db_session.query(ModelProductRetailer).all()
            return product_retailers
        except Exception as e:
            self.log.error(f"Error getting product retailers: {e}")
            raise Exception(f"Error getting product retailers: {e}")
