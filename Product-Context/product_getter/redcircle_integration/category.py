from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging
from typing import Any, Dict, List
from redcircle_integration.external_sources.api_object import ApiSources
from product_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase

@dataclass
class CategoryAttributes:
    id: str
    name: str
    has_children: bool
    
    @property
    def is_leaf_category(self) -> bool:
        return not self.has_children


class Category(ABC):
    def __init__(self, api_object, object_database,**kwargs) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info(f"Category class called")
        self.api_object:ApiSources =  api_object
        self.object_database:ObjectDataBase = object_database

        
    @abstractmethod
    def pull_categories(self) -> Dict:
       pass
    
    @abstractmethod
    def save_in_db(self) -> None:
        pass
    
        
        

