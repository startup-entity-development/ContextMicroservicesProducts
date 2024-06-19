
import logging
from typing import List
from product_ctx_database_sqlalchemy_14.models.category_model import ModelCategory
from product_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase
from product_ctx_database_sqlalchemy_14.objects.utils import normalize_string


class CategoryDataBase(ObjectDataBase):
    def __init__(self, db_session, log):
        super().__init__(db_session, log)

    def create_id_api(self, name:str) -> str:
        return normalize_string(name)

    def create(self,
               api_id:str,
               name:str,
               description:str,
               default_base_increment:float,
               auto_commit:bool=True) -> ModelCategory:
        """Create category model."""
        try:
            category = ModelCategory(
                api_id= self.create_id_api(name),
                name=name,
                default_base_increment=default_base_increment,
                description=description,)
                
            self.db_session.add(category)
            if auto_commit: 
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.db_session.refresh(category)
            self.log.info(f"create_category done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, create_category fail {e}")
        return category

    def delete_all(self, auto_commit:bool= True) -> None:
        """Delete all categories."""
        try:
            self.db_session.query(ModelCategory).delete()
            if auto_commit:
                self.db_session.commit()
            self.log.info(f"delete_all_categories done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, delete_all_categories fail {e}")        

    def get(self, id:int) -> ModelCategory:
        """Get category model."""
        try:
            category = self.db_session.query(ModelCategory).filter_by(api_id=id).first()
            self.log.info(f"get_category done")
            return category
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_category fail {e}")  
    
    def get_by_name(self, name:str) -> ModelCategory:
        """Get category model."""
        try:
            category = self.db_session.query(ModelCategory).filter_by(name=name).first()
            self.log.info(f"get_category done")
            return category
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_category fail {e}")      
    
    def get_all(self) -> List[ModelCategory]:
        """Get all categories model."""
        try:
            categories = self.db_session.query(ModelCategory).all()
            self.log.info(f"get_all_categories done")
            return categories
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_all_categories fail {e}")

    def delete(self, id_category:int, auto_commit:bool= True):
        # delete category
        try:
            category = self.db_session.query(ModelCategory).get(id_category)
            self.db_session.delete(category)
            if auto_commit:
                self.db_session.commit()
            
            self.log.info(f"delete_category done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, delete_category fail {e}")
    
    def get_by_id_api(self, id_api:str) -> ModelCategory:
        """Get category model."""
        try:
            category = self.db_session.query(ModelCategory).filter_by(api_id=id_api).first()
            self.log.info(f"get_category done")
            return category
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_category fail {e}")
