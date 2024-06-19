

from dataclasses import dataclass
from typing import Any, List
from product_ctx_database_sqlalchemy_14.models.base import db_session
from product_ctx_database_sqlalchemy_14.models.retailer_model import ModelRetailer
from product_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase


@dataclass
class RetailerAttributes:
    name: str
    description: str

    @property
    def model_dictionary(self) -> dict:
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

    def create(self, retailer_attributes: RetailerAttributes) -> Any:
        self.log.info("Creating retailer")
        try:
            retailer_model = ModelRetailer(**retailer_attributes.model_dictionary)
            self.db_session.add(retailer_model)
            self.db_session.commit()
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
        
    