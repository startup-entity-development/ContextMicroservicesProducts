

from dataclasses import dataclass
from typing import Any
from product_ctx_database_sqlalchemy_14.models.media_model import ModelMedia
from product_ctx_database_sqlalchemy_14.models.base import db_session
from product_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase


@dataclass
class MediaAttributes(): 
    product_id:int
    media_type:str
    name:str
    description:str
    link_url:str 
    is_main:bool
    
    @property
    def model_dictionary(self)->dict:
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelMedia.__dict__.keys()
        }

@dataclass
class MediaAttributesGateway(): 
    
    def __init__(self, **kwargs):
        self.product_id:int
        self.media_type:str
        self.name:str
        self.description:str
        self.link_url:str 
        self.is_main:bool
        
    @property
    def model_dictionary(self)->dict:
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelMedia.__dict__.keys()
        }
        
    def from_dict(self, obj_dict:dict):
        self.__dict__.update(obj_dict)
        return self

class MediaDataBase(ObjectDataBase):
    
    def __init__(self, log):
        self.log = log
        self.db_session = db_session
        super().__init__(self.db_session, self.log)
    
    def create(self, media:MediaAttributes, auto_commit:bool= True) -> ModelMedia|None:
        """Create media."""
        try:
            media_dict = media.model_dictionary   
            media = ModelMedia(**media_dict)
            self.db_session.add(media)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.log.info(f"create_media done")
            return media
        
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: setup_db.py method:, create_media fail {e}")
            raise None
        
    def delete(self, id:int, auto_commit:bool= True) -> None:
        """Delete media."""
        try:
            media = self.db_session.query(ModelMedia).filter_by(id=id).first()
            self.db_session.delete(media)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.log.info(f"delete_media done")
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: setup_db.py method:, delete_media fail {e}")
            raise None
        
    def get(self, id: int) -> Any:
        return super().get(id)
    
    def get_all(self) -> Any:
        return super().get_all()
    
    def delete_all(self, auto_commit:bool= True) -> None:
        return super().delete_all(auto_commit)
