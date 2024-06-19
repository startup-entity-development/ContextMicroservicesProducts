from dataclasses import dataclass
from enum import Enum, EnumType
from logging import Logger
import time
from typing import Any, Dict, List

from graphql_relay import from_global_id
from product_ctx_database_sqlalchemy_14.models.product_model import ModelProduct
from product_ctx_database_sqlalchemy_14.models.base import db_session
from datetime import datetime
from product_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase
from product_ctx_database_sqlalchemy_14.objects.utils import UnitMeasure

    

@dataclass
class ProductAttributes(): 
    sub_category_id:int
    title:str
    brand:str
    base_increment:float
    description:str
    upc_barcode:str
    id:int|str = None
    api_id:str = None
    name:str = None
    unit_measure:UnitMeasure = None
    weight:float = None
    size:str = None
    unit_in_pack:int = 1
    dpci:str = None 
    tcin:int = None
    words_tags:str = None
    is_active:bool = True

    def __decode_id(self, id:int|str)->int:
        if isinstance(id, str):
            id = int(from_global_id(id).id)
        return id
    
    @property
    def model_dictionary(self) ->dict:
        obj_dict = self.__dict__.copy()
        obj_dict["sub_category_id"] = self.__decode_id(obj_dict["sub_category_id"])
        obj_dict["id"] = self.__decode_id(obj_dict["id"])

        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelProduct.__dict__.keys()
        }
    
    @staticmethod
    def from_dict(obj_dict: Dict):
        return ProductAttributes(**obj_dict)
    

class ProductDatabase(ObjectDataBase):

    def __init__(self, log):
        self.log = log
        self.db_session = db_session
        super().__init__(self.db_session, self.log)
    
    def __update_default_words_tags(self, product_dict:Dict[str,Any], default_words_tags:str) -> Dict[str,Any]:
        assert isinstance(default_words_tags, str), "default_words_tags must be a string, fucntion: __update_default_words_tags"
        assert isinstance(product_dict, dict), "product_dict must be a dictionary, fucntion: __update_default_words_tags"
        if product_dict.get("words_tags") is None:
                product_dict["words_tags"] = default_words_tags
        return product_dict
    
    def __update_unit_measure(self, product_dict:Dict[str,Any], unit_measure:UnitMeasure) -> Dict[str,Any]:
        assert isinstance(product_dict, dict), "product_dict must be a dictionary, fucntion: __update_unit_measure"
        if product_dict.get("unit_measure") is None:
                product_dict["unit_measure"] = unit_measure
        return product_dict
    
    def __update_name(self, product_dict:Dict[str,Any],) -> Dict[str,Any]:
        assert isinstance(product_dict, dict), "product_dict must be a dictionary, fucntion: __update_name"
        if product_dict["name"] is None:
                product_dict["name"] = product_dict["title"]
        return product_dict
    
    def create(self, 
               product_attr:ProductAttributes,
               auto_commit:bool= True,
               raise_integrity_except=False,
               default_words_tags:str="" ) -> ModelProduct|None:
        
        """Create product."""
        now = int(time.time())
        try:
            product_dict = product_attr.model_dictionary
            product_dict["created"] = now
            product_dict = self.__update_default_words_tags(product_dict, default_words_tags)
            product_dict = self.__update_unit_measure(product_dict, product_attr.unit_measure)
            product_dict = self.__update_name(product_dict)
            product_model = ModelProduct(**product_dict)
            self.db_session.add(product_model)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.db_session.refresh(product_model)
            self.log.info(f"create_product done")
            return product_model        
           
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError":
                self.db_session.rollback()
                self.log.error(f"create product IntegrityError duplicate key value violates unique constraint product : {product_attr.title}")
                if raise_integrity_except:
                    raise Exception(f"create product IntegrityError duplicate key value violates unique constraint product : {product_attr.title}")
                return None
            
            raise Exception(f"file: setup_db.py method:, create_product fail {e}")
            
    def delete(self, id:int, auto_commit:bool= True) -> None:
        """Delete product."""
        try:
            product = self.db_session.query(ModelProduct).filter_by(id=id).first()
            self.db_session.delete(product)
            if auto_commit:
                self.db_session.commit()
            self.log.info(f"delete_product done")
        except Exception as e:
            messageException = f"file: setup_db.py method:, delete_product fail {e}"
            self.log.error(messageException)
            raise Exception(messageException)
        
    def get(self, id:int) -> ModelProduct:
        """Get product by id."""
        try:
            product = self.db_session.query(ModelProduct).filter_by(id=id).first()
            self.log.info(f"get_product_by_id done")
            return product
        except Exception as e:
            messageException = f"file: setup_db.py method:, get_product_by_id fail {e}"
            self.log.error(messageException)
            raise Exception(messageException)
        
    def get_by_tcin(self, tcin:int) -> ModelProduct:
        """Get product by tcin."""
        try:
            product = self.db_session.query(ModelProduct).filter_by(tcin=tcin).first()
            self.log.info(f"get_product_by_tcin done")
            return product
        except Exception as e:
            messageException = f"file: setup_db.py method:, get_product_by_tcin fail {e}"
            self.log.error(messageException)
            raise Exception(messageException)
        
    def delete_all(self, auto_commit:bool= True) -> None:
        """Delete all products."""
        try:
            self.db_session.query(ModelProduct).delete()
            if auto_commit:
                self.db_session.commit()
            self.log.info(f"delete_all_products done")
        except Exception as e:
            messageException = f"file: setup_db.py method:, delete_all_products fail {e}"
            self.log.error(messageException)
            raise Exception(messageException)
        
    def get_product_by_sub_category_id(self, sub_category_id:int) -> list:
        """Get product by sub_category_id."""
        try:
            products = self.db_session.query(ModelProduct).filter_by(sub_category_id=sub_category_id).all()
            self.log.info(f"get_product_by_sub_category_id done")
            return products
        except Exception as e:
            messageException = f"file: setup_db.py method:, get_product_by_sub_category_id fail {e}"
            self.log.error(messageException)
            raise Exception(messageException)
    
    def get_product_by_api_id(self, api_id:str) -> ModelProduct:
        """Get product by api_id."""
        try:
            product = self.db_session.query(ModelProduct).filter_by(api_id=api_id).first()
            self.log.info(f"get_product_by_api_id done")
            return product
        except Exception as e:
            messageException = f"file: setup_db.py method:, get_product_by_api_id fail {e}"
            self.log.error(messageException)
            raise Exception(messageException)        
   
    def get_all(self) -> List[Any]:
        """Get all products."""
        try:
            products = self.db_session.query(ModelProduct).all()
            self.log.info(f"get_all_products done")
            return products
        except Exception as e:
            messageException = f"file: setup_db.py method:, get_all_products fail {e}"
            self.log.error(messageException)
            raise Exception(messageException)
        
    def update(self, product_attr:ProductAttributes,
                auto_commit:bool= True,
                default_words_tags:str="") -> ModelProduct:
        """Update product."""
        now = int(time.time())

        try:
            product_dict = product_attr.model_dictionary
            product_dict["edited"] = now
            id:int = product_dict["id"]
            product_dict = self.__update_default_words_tags(product_dict, default_words_tags)
            product_dict = self.__update_unit_measure(product_dict, product_attr.unit_measure)
            product_dict = self.__update_name(product_dict)
            self.db_session.query(ModelProduct).filter_by(id=id).update(product_dict)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            product_model = self.db_session.query(ModelProduct).filter_by(id=id).first()
            self.log.info(f"update_product done")
            return product_model
        except Exception as e:
            messageException = f"file: setup_db.py method:, update_product fail {e}"
            self.log.error(messageException)
            raise Exception(messageException)