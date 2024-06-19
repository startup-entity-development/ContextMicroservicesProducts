

from dataclasses import dataclass
from typing import Any, List
from product_ctx_database_sqlalchemy_14.models.base import db_session
from product_ctx_database_sqlalchemy_14.models.retailer_model import ModelRetailer
from product_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase


@dataclass
class RetailerAttributes:
    """ Retailer Attributes """
    name: str
    description: str

    def format_name(self) -> str:
        self.name = self.name.lower()
        self.name = self.name.strip()
        # capitalize the first letter of each word
        self.name = self.name.title()
        return self.name
    


    @property
    def model_dictionary(self) -> dict:
        self.format_name()
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelRetailer.__dict__.keys()
        }

class RetailerDatabase(ObjectDataBase):

    def __init__(self, log):
        self.log = log
        self.db_session = db_session
        super().__init__(self.db_session, self.log)

    def create(self, retailer_attributes: RetailerAttributes, auto_commit:bool= True) -> Any:
        self.log.info("Creating retailer")
        try:
            retailer_model = ModelRetailer(**retailer_attributes.model_dictionary)
            self.db_session.add(retailer_model)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.db_session.refresh(retailer_model)
            return retailer_model
        except Exception as e:
            self.log.error(f"Error creating retailer: {e}")
            raise Exception(f"Error creating retailer: {e}")
        
        return self.save(retailer_model)
    
    def get(self, retailer_id: int) -> Any:
        self.log.info("Getting retailer")
        try:
            retailer = self.db_session.query(ModelRetailer).filter(ModelRetailer.id == retailer_id).first()
        except Exception as e:
            self.log.error(f"Error getting retailer: {e}")
            raise Exception(f"Error getting retailer: {e}")
        
        return retailer
    
    def get_by_name(self, name: str) -> Any:
        self.log.info("Getting retailer by name")
        RetailerAttributes(name=name, description="")
        name:str = RetailerAttributes(name=name, description="").format_name()
        try:
            retailer = self.db_session.query(ModelRetailer).filter(ModelRetailer.name == name).first()
        except Exception as e:
            self.log.error(f"Error getting retailer by name: {e}")
            raise Exception(f"Error getting retailer by name: {e}")
        
        return retailer
    
    def get_by_api_name(self, api_name: str) -> List[ModelRetailer]:
        self.log.info("Getting retailer by api name")
        try:
            retailers = self.db_session.query(ModelRetailer).filter(ModelRetailer.api_name == api_name).all()
        except Exception as e:
            self.log.error(f"Error getting retailer by api name: {e}")
            raise Exception(f"Error getting retailer by api name: {e}")
        
        return retailers
    
    def get_all(self) -> List[ModelRetailer]:
        
        try:
            self.log.info("Getting retailers")
            retailers = self.db_session.query(ModelRetailer).all()
        except Exception as e:
            self.log.error(f"Error getting retailers: {e}")
            raise Exception(f"Error getting retailers: {e}")
        return retailers    

    def delete_all(self, auto_commit: bool = True) -> None:
        try:
            self.log.info("Deleting all retailers")
            self.db_session.query(ModelRetailer).delete()
            if auto_commit:
                self.db_session.commit()
        except Exception as e:
            self.log.error(f"Error deleting all retailers: {e}")
            raise Exception(f"Error deleting all retailers: {e}")
    
    def delete(self, retailer_id: int, auto_commit: bool = True) -> None:
        try:
            self.log.info("Deleting retailer")
            retailer = self.db_session.query(ModelRetailer).filter(ModelRetailer.id == retailer_id).first()
            self.db_session.delete(retailer)
            if auto_commit:
                self.db_session.commit()
        except Exception as e:
            self.log.error(f"Error deleting retailer: {e}")
            raise Exception(f"Error deleting retailer: {e}")
        
    
        
    