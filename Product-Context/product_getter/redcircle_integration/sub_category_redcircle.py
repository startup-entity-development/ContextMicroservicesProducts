from typing import Any, Dict, List
from product_ctx_database_sqlalchemy_14.models.category_model import ModelCategory
from product_ctx_database_sqlalchemy_14.models.sub_category_model import ModelSubCategory
from product_ctx_database_sqlalchemy_14.objects.sub_category_object import SubCategoryDataBase
from redcircle_integration.category_redcircle import CategoryRedCircle


class SubCategoryRedCircle(CategoryRedCircle):
    
    def __init__(self,object_database: SubCategoryDataBase) -> None:
        super().__init__(object_database)
        self.object_database:SubCategoryDataBase
    
    def update_database(self, id_api_category:str,
                              id_category:int,
                              only_if_has_children:bool=True) -> List[ModelCategory]:
        
        self.pull_categories(main_category_id=id_api_category)
        dict_subcategory_image:Dict[str, str] =self.get_dict_image_subcategory_from_csv()
        for category_attributes in self.list_red_circle_attributes:
                image = self.get_image_from_dict_subcategory(name_subcategory=category_attributes.name,
                                                             dict_subcategory_image=dict_subcategory_image)
                                                           
                self.object_database.create(api_id=category_attributes.id,
                                        id_category=id_category,
                                        name=category_attributes.name,
                                        image=image ,
                                        description=category_attributes.name,
                                        default_base_increment=13.0,
                                        auto_commit=False)
                
        self.object_database.save_session_database()
        
    def create_categories_cvs_file_bunch_request(self):
        subcategories_list:List[ModelSubCategory] = self.object_database.get_all()
        f = open("category_collection_redcircle.cvs", "a")
        for subcategory in subcategories_list:
            f.write(f'\n "{subcategory.api_id}","category",100,,,,,,,,,,,,,,,,')
        f.close()
        
            
    def get_dict_image_subcategory_from_csv(self) -> Dict[str, str]:
        dict_subcategory_image:Dict[str, str] = {}  
        f = open("subcategory_name_image.csv", "r")
        for line in f:
            image, name = line.split("|")
            #avoid first line with headers
            if name == "name":
                continue
            #remove \n from name
            name = name.replace("\n", "")
            dict_subcategory_image[name] = image
        f.close()
        return dict_subcategory_image
    
    def get_image_from_dict_subcategory(self, name_subcategory:str, dict_subcategory_image:Dict[str, str]) -> str:        
        return dict_subcategory_image.get(name_subcategory)