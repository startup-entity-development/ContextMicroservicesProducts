from abc import ABC, abstractmethod
from dataclasses import dataclass
from json import dumps, loads
import logging
from typing import Any, List
from product_ctx_database_sqlalchemy_14.objects.product_object import ProductAttributes, ProductDatabase
from data_source_integrations.external_sources.api_object import ApiSources
from data_source_integrations.media import ImageResult, VideoResult
from data_source_integrations.pagination.pagination import Pagination
    
@dataclass
class ProductResult:
    title:str
    link:str
    dpci:str
    tcin:int
    price:float
    brand:str
    feature_bullets:List[str]
    images:List[ImageResult]
    videos:List[VideoResult]

@dataclass
class ProductResultDetailled():
    tcin:int
    upc:str
    description:str

    
@dataclass
class ProductFileSubCategoryResult:
    id_subcategory_api:str
    products:List[ProductResult]

    
@dataclass
class ProductSearchResult:
    pagination:Pagination
    products:List[ProductResult]

@dataclass
class ProductAttributesMedia():
    product_attributes:ProductAttributes
    images:List[ImageResult]
    videos:List[VideoResult]
    
    
class Product(ABC):
    def __init__(self, api_object, **kwargs) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info(f"Product class called")
        self.api_object:ApiSources =  api_object
        self.object_database: ProductDatabase = ProductDatabase(log=self.log)
        
        
    @abstractmethod
    def _pull_products_raw(self, id_subcategory) -> Any:
       pass
    
    
    @abstractmethod
    def update_database_from_request(self) -> None:
        pass
    
@dataclass  
class ResultGetFromAPI():
    id_database:int
    id_api:str
    term:str
    
    @property
    def json_string(self):
        return dumps({
            "id_database": self.id_database,
            "id_api": self.id_api,
        "term": self.term
        }) 

