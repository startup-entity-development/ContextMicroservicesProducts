

import time
from product_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase
from product_ctx_database_sqlalchemy_14.models.base import db_session
from product_ctx_database_sqlalchemy_14.models.retailer_location_model import ModelRetailerLocation
from dataclasses import dataclass
from typing import Dict


@dataclass
class LocationRetailerAttributes:
    """ Location Retailer Attributes """
    retailer_id:int
    street_addr:str
    city:str
    state:str
    zipcode:str
    country:str
    latitude:float
    longitude:float
    is_active:bool
    created:int
    updated:int

    @property
    def model_dictionary(self) -> dict:
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelRetailerLocation.__dict__.keys()
        }
    
    @staticmethod
    def from_dict(obj_dict: Dict):
        return LocationRetailerAttributes(**obj_dict)

class LocationRetailerDataBase(ObjectDataBase):
    
    def __init__(self,log):
        self.log = log
        self.db_session = db_session
        super().__init__(self.db_session, self.log)
    
    def create(self, location_retailer_attributes:LocationRetailerAttributes, auto_commit = True)->ModelRetailerLocation:
        try:
            now = int(time.time())
            location_retailer_attributes.created = now
            location_retailer_model:ModelRetailerLocation = ModelRetailerLocation(**location_retailer_attributes.model_dictionary)
            self.db_session.add(location_retailer_model)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.db_session.refresh(location_retailer_model)
            return location_retailer_model
        except Exception as e:
            self.log.error(f"Error creating location retailer: {e}")
            raise Exception(f"Error creating location retailer: {e}")
    
    def get(self, location_retailer_id:int)->ModelRetailerLocation:
        try:
            location_retailer_model:ModelRetailerLocation = self.db_session.query(ModelRetailerLocation).filter(ModelRetailerLocation.id == location_retailer_id).first()
            return location_retailer_model
        except Exception as e:
            self.log.error(f"Error getting location retailer: {e}")
            raise Exception(f"Error getting location retailer: {e}")

    def get_by_retailer_id(self, retailer_id:int)->ModelRetailerLocation:
        try:
            location_retailer_model:ModelRetailerLocation = self.db_session.query(ModelRetailerLocation).filter(ModelRetailerLocation.retailer_id == retailer_id).first()
            return location_retailer_model
        except Exception as e:
            self.log.error(f"Error getting location retailer by retailer id: {e}")
            raise Exception(f"Error getting location retailer by retailer id: {e}")

    def update(self, location_retailer_id:int, location_retailer_attributes:LocationRetailerAttributes, auto_commit = True)->ModelRetailerLocation:
        try:
            now = int(time.time())
            location_retailer_attributes.updated = now
            location_retailer_model:ModelRetailerLocation = self.get(location_retailer_id)
            for key, value in location_retailer_attributes.model_dictionary.items():
                setattr(location_retailer_model, key, value)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.db_session.refresh(location_retailer_model)
            return location_retailer_model
        except Exception as e:
            self.log.error(f"Error updating location retailer: {e}")
            raise Exception(f"Error updating location retailer: {e}")

    def delete(self, location_retailer_id:int, auto_commit = True):
        try:
            location_retailer_model:ModelRetailerLocation = self.get(location_retailer_id)
            self.db_session.delete(location_retailer_model)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
        except Exception as e:
            self.log.error(f"Error deleting location retailer: {e}")
            raise Exception(f"Error deleting location retailer: {e}")

    def delete_all(self, auto_commit: bool = True) -> None:
        return super().delete_all(auto_commit)

    def get_all(self):
        return super().get_all()
    
