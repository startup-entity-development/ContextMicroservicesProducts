import logging
from typing import List
from product_ctx_database_sqlalchemy_14.models.sub_category_model import ModelSubCategory
from product_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase

        
class SubCategoryDataBase(ObjectDataBase):
    
    def __init__(self, db_session, log:logging.Logger):
        super().__init__(db_session, log)
    

     
    def create(self,api_id:str,
               id_category:int,
               name:str,
               description:str,
               image:str,
               default_base_increment:float,
               auto_commit:bool=True) -> ModelSubCategory:
        
        
        """Create subcategory model."""
        try:
            sub_category = ModelSubCategory(
                category_id=id_category,
                api_id=api_id,
                name=name,
                image=image,
                description=description,
                default_base_increment=default_base_increment
                )
            
            self.db_session.add(sub_category)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.log.info(f"create_sub_category done")
            self.db_session.refresh(sub_category)
            return sub_category
        
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, create_sub_category fail {e}")
        
    def delete_all(self, auto_commit:bool= True) -> None:
        """Delete all subcategories."""
        try:
            self.db_session.query(ModelSubCategory).delete()
            if auto_commit:
                self.db_session.commit()
            self.log.info(f"delete_all_subcategories done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, delete_all_subcategories fail {e}")        

    def get(self, id:int) -> ModelSubCategory:
        """Get subcategory model."""
        try:
            subcategory = self.db_session.query(ModelSubCategory).filter_by(id=id).first()
            self.log.info(f"get_subcategory done")
            return subcategory
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_subcategory fail {e}")     
    
    def get_by_id_api(self, id_api:str) -> ModelSubCategory:
        """Get subcategory model."""
        try:
            subcategory = self.db_session.query(ModelSubCategory).filter_by(api_id=id_api).first()
            self.log.info(f"get_subcategory done")
            return subcategory
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_subcategory fail {e}")     
    
    def get_by_category_id(self,category_id:int) -> List[ModelSubCategory]:
        """Get all sub categories model."""
        try:
            subcategories = self.db_session.query(ModelSubCategory).filter_by(category_id=category_id).all()
            self.log.info(f"get_all_categories done")
            return subcategories
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_all_sub_categories fail {e}")
    
    def get_all(self) -> List[ModelSubCategory]:
        """Get all sub categories model."""
        try:
            subcategories = self.db_session.query(ModelSubCategory).all()
            self.log.info(f"get_all_categories done")
            return subcategories
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_all_sub_categories fail {e}")
            
    
    def delete(self, id_subcategory:int, auto_commit:bool= True):
        """delete subcategory"""
        try:
            subcategory = self.db_session.query(ModelSubCategory).get(id_subcategory)
            self.db_session.delete(subcategory)
            if auto_commit:
                self.db_session.commit()
            
            self.log.info(f"delete_category done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, delete_category fail {e}")
