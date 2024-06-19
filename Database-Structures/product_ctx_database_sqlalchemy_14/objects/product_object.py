from dataclasses import dataclass
from enum import Enum, EnumType
from logging import Logger
import time
from typing import Any, List
from product_ctx_database_sqlalchemy_14.models.product_model import ModelProduct
from product_ctx_database_sqlalchemy_14.models.base import db_session
from datetime import datetime
from product_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase

class UnitMeasure(Enum):
    """Unit measure."""
    oz = "ounce"
    lb = "pound"
    fl = "ounce"
    kg = "kilo"
    gal = "gallon"
    ml =  "milliliter"
    g =  "gram"
    l =   "liter"
    
        


@dataclass
class ProductAttributes(): 
    sub_category_id:int
    api_id:str
    name:str
    title:str
    brand:str
    base_increment:float
    description:str
    upc_barcode:str
    unit_measure:UnitMeasure
    weight:float
    size:str 
    unit_in_pack:int
    cost:float
    dpci:str 
    tcin:int
    words_tags:str = None

    
    @property
    def model_dictionary(self) ->dict:
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelProduct.__dict__.keys()
        }

@dataclass
class ProductAttributesGateway(): 
    
    def __init__(self, **kwargs):
        self.sub_category_id:int
        self.api_id:str
        self.name:str
        self.title:str
        self.brand:str
        self.base_increment:float
        self.description:str
        self.upc_barcode:str
        self.unit_measure:UnitMeasure
        self.weight:float
        self.size:str
        self.unit_in_pack:int
        self.dpci:str
        self.tcin:int
        self.words_tags:str = None

     
         
    
    @property
    def model_dictionary(self)->dict:
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelProduct.__dict__.keys()
        }
    
    def from_dict(self, obj_dict:dict):
        self.__dict__.update(obj_dict)
        return self

class ProductDatabase(ObjectDataBase):

    def __init__(self, log):
        self.log = log
        self.db_session = db_session
        super().__init__(self.db_session, self.log)
        
    def create(self, product:ProductAttributesGateway, auto_commit:bool= True, raise_integrity_except=False) -> ModelProduct|None:
        """Create product."""
        now = int(time.time())
        try:
            product_dict = product.model_dictionary   
            product_dict["name"] = product.title
            product_dict["created"] = now
            if product_dict.get("words_tags") is None:
                product_dict.pop("words_tags")
            if isinstance(product_dict["unit_measure"], UnitMeasure):
                product_dict["unit_measure"] = product_dict["unit_measure"].value
            product = ModelProduct(**product_dict)
            self.db_session.add(product)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.log.info(f"create_product done")
            return product           
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError":
                self.db_session.rollback()
                self.log.error(f"create product IntegrityError duplicate key value violates unique constraint product : {product.title}")
                if raise_integrity_except:
                    raise Exception(f"create product IntegrityError duplicate key value violates unique constraint product : {product.title}")
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