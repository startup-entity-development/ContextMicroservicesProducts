

from dataclasses import dataclass
import logging
from typing import Any, Dict, List
from product_ctx_database_sqlalchemy_14.models.category_model import ModelCategory
from product_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase
from redcircle_integration.category import Category, CategoryAttributes
from redcircle_integration.external_sources.api_red_circle import RedCircle


@dataclass
class RedCircleAttributes(CategoryAttributes):
    is_root: bool
    path: str
    link: str
    parent_id: str
    parent_name: str
    type: str
    domain: str


class CategoryRedCircle(Category):
    
    def __init__(self, object_database:ObjectDataBase) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info(f"CategoryRedCircle class called")
        self.api_object:RedCircle = RedCircle()
        self.list_red_circle_attributes:List[RedCircleAttributes] = []
        super().__init__(api_object=self.api_object, object_database=object_database)

    def get_grocery_id(self, )->str:
        return self.api_object.get_main_category_id(name_main_category="Grocery",
                                                    list_dict_main_categories=self.api_object.get_main_categories())

    def pull_categories(self,main_category_id:str=None) -> List[CategoryAttributes]:   
        self.list_red_circle_attributes.clear()
        if not main_category_id:
            main_category_id = self.get_grocery_id()
            
        list_categories_dict:List[Dict[str, Any]] = self.api_object.get_categories(main_category_id=main_category_id)
        
        for category in list_categories_dict:
            category_attributes = RedCircleAttributes(**category)
            self.list_red_circle_attributes.append(category_attributes)
            self.log.info(f"category_attributes: {category_attributes}")


    def save_in_db(self, only_if_has_children:bool=True) -> List[ModelCategory]:
        if self.list_red_circle_attributes.__len__() == 0:
            self.pull_categories()
            
        for category_attributes in self.list_red_circle_attributes:
            if category_attributes.has_children and only_if_has_children:    
                self.object_database.create(api_id=category_attributes.id,
                                        name=category_attributes.name,
                                        description=category_attributes.name,
                                        default_base_increment=13.0,
                                        auto_commit=False)
            
            
        self.object_database.save_session_database()
