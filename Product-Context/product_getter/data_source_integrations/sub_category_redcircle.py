from typing import Any, Dict, List
from product_ctx_database_sqlalchemy_14.models.category_model import ModelCategory
from product_ctx_database_sqlalchemy_14.models.sub_category_model import ModelSubCategory
from product_ctx_database_sqlalchemy_14.objects.sub_category_object import SubCategoryDataBase
from data_source_integrations.category_redcircle import CategoryRedCircle


class SubCategoryRedCircle(CategoryRedCircle):
    
    def __init__(self,object_database: SubCategoryDataBase) -> None:
        super().__init__(object_database)
        self.object_database:SubCategoryDataBase
    
    def update_database(self, id_api_category:str,
                              id_category:int,
                              only_if_has_children:bool=True) -> List[ModelCategory]:
        
        self.pull_categories(main_category_id=id_api_category)
            
        for category_attributes in self.list_red_circle_attributes:
                self.object_database.create(api_id=category_attributes.id,
                                        id_category=id_category,
                                        name=category_attributes.name,
                                        description=category_attributes.name,
                                        auto_commit=False)
            
            
        self.object_database.save_session_database()
        
    def create_categories_cvs_file_buch_request(self):
        subcategories_list:List[ModelSubCategory] = self.object_database.get_all()
        f = open("category_collection_redcircle.cvs", "a")
        for subcategory in subcategories_list:
            f.write(f'\n "{subcategory.api_id}","category",100,,,,,,,,,,,,,,,,')
        f.close()
        
            
        