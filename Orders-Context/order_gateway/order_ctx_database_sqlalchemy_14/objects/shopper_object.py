
from typing import List
from order_ctx_database_sqlalchemy_14.models.shopper import ModelShopper
from order_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase
from order_ctx_database_sqlalchemy_14.models.base import db_session
from typing import Optional

class ShopperAttributesGateway(): 
    
    def __init__(self, **kwargs):
        self.name:str
    
    @property
    def model_dictionary(self)->dict:
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelShopper.__dict__.keys()
        }
    
    def from_dict(self, obj_dict:dict):
        self.__dict__.update(obj_dict)
        return self


class ShopperDataBase(ObjectDataBase):
    def __init__(self, log):
        self.log = log
        self.db_session = db_session
        super().__init__(db_session, log)

    def create(self, shopper:ShopperAttributesGateway, auto_commit:bool= True, raise_integrety_except=False) -> Optional[ModelShopper]:
        """Create shopper."""
        try:
            shopper_dict = shopper.model_dictionary   
            shopper_dict["name"] = shopper.name
            
            shopper = ModelShopper(**shopper_dict)
            self.db_session.add(shopper)

            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.log.info(f"create_shopper done")
            return shopper           
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: setup_db.py method:, create_shopper fail {e}")
            if raise_integrety_except:
                raise e
            raise None

    def delete_all(self, auto_commit:bool= True) -> None:
        """Delete all shoppers."""
        try:
            self.db_session.query(ModelShopper).delete()
            if auto_commit:
                self.db_session.commit()
            self.log.info(f"delete_all_shoppers done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, delete_all_shoppers fail {e}")        

    def get(self, id:int) -> ModelShopper:
        """Get shopper model."""
        try:
            shopper = self.db_session.query(ModelShopper).filter_by(id=id).first()
            self.log.info(f"get_shopper done")
            return shopper
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_shopper fail {e}")     
    
    def get_all(self) -> List[ModelShopper]:
        """Get all shoppers model."""
        try:
            shoppers = self.db_session.query(ModelShopper).all()
            self.log.info(f"get_all_shoppers done")
            return shoppers
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_all_shoppers fail {e}")
            
    
    def delete(self, id_shopper:int, auto_commit:bool= True):
        # delete shopper
        try:
            shopper = self.db_session.query(ModelShopper).get(id_shopper)
            self.db_session.delete(shopper)
            if auto_commit:
                self.db_session.commit()
            
            self.log.info(f"delete_shopper done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, delete_shopper fail {e}")

    def create_default_shoppers(self):
        """Create default shoppers."""
        try:
            shopper = ShopperAttributesGateway()
            shopper.name = "default"
            self.create(shopper, auto_commit=False)
            self.db_session.commit()
            self.log.info(f"create_default_shoppers done")
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: setup_db.py method:, create_default_shoppers fail {e}")
