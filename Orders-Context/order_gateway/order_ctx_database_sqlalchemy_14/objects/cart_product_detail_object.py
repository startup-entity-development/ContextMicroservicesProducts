
from typing import List
from order_ctx_database_sqlalchemy_14.models.cart_product_detail import ModelCartProductDetail
from order_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase
from order_ctx_database_sqlalchemy_14.models.base import db_session
from typing import Optional
from datetime import datetime

class CartProductDetailAttributesGateway(): 
    
    def __init__(self, **kwargs):
        self.quantity:int
        self.price:str
        self.product_added_date:str
        self.cart_id:str
        self.product_id:str
        self.retailer_id:str
        self.retailer_name:str
        self.preference_product:str
    
    @property
    def model_dictionary(self)->dict:
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelCartProductDetail.__dict__.keys()
        }
    
    def from_dict(self, obj_dict:dict):
        self.__dict__.update(obj_dict)
        return self

class CartProductDetailDataBase(ObjectDataBase):
    def __init__(self, log):
        self.log = log
        self.db_session = db_session
        super().__init__(db_session, log)
        
    def create(self, cart_product_detail:CartProductDetailAttributesGateway, auto_commit:bool= True, raise_integrety_except=False) -> Optional[ModelCartProductDetail]:        
        """Create cart product detail model."""
        try:
            cart_product_detail_dict = cart_product_detail.model_dictionary
            cart_product_detail_dict["product_added_date"] = datetime.now()
            cart_product_detail = ModelCartProductDetail(**cart_product_detail_dict)
            self.db_session.add(cart_product_detail)

            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.log.info(f"create_cart done")
            return cart_product_detail           
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: setup_db.py method:, create_cart fail {e}")
            if raise_integrety_except:
                raise e
            raise None

    def delete_all(self, auto_commit:bool= True) -> None:
        """Delete all cart_product_details."""
        try:
            self.db_session.query(ModelCartProductDetail).delete()
            if auto_commit:
                self.db_session.commit()
            self.log.info(f"delete_all_cart_product_details done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, delete_all_cart_product_details fail {e}")        

    def get(self, id:int) -> ModelCartProductDetail:
        """Get cart_product_detail model."""
        try:
            cart_product_detail = self.db_session.query(ModelCartProductDetail).filter_by(id=id).first()
            self.log.info(f"get_cart_product_detail done")
            return cart_product_detail
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_cart_product_detail fail {e}")     
    
    def get_all(self) -> List[ModelCartProductDetail]:
        """Get all cart_product_details model."""
        try:
            cart_product_details = self.db_session.query(ModelCartProductDetail).all()
            self.log.info(f"get_all_cart_product_details done")
            return cart_product_details
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_all_cart_product_details fail {e}")
            
    
    def delete(self, id_cart_product_detail:int, auto_commit:bool= True):
        # delete cart_product_detail
        try:
            cart_product_detail = self.db_session.query(ModelCartProductDetail).get(id_cart_product_detail)
            self.db_session.delete(cart_product_detail)
            if auto_commit:
                self.db_session.commit()
            
            self.log.info(f"delete_cart_product_detail done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, delete_cart_product_detail fail {e}")

    def get_by_cart_and_product(self, cart_id:int, product_id:int) -> ModelCartProductDetail:
        """Get cart_product_detail model."""
        try:
            cart_product_detail = self.db_session.query(ModelCartProductDetail)\
                .filter(ModelCartProductDetail.cart_id==cart_id)\
                .filter(ModelCartProductDetail.product_id==product_id)\
                .first()
            self.log.info(f"get_by_cart_and_product done")
            return cart_product_detail
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_by_cart_and_product fail {e}")

    def update(self, cart_product_detail_id, cart_product_detail:CartProductDetailAttributesGateway, auto_commit:bool= True, raise_integrety_except=False) -> Optional[ModelCartProductDetail]:        
        """Update cart product detail model."""
        try:
            cart_product_detail_model = self.db_session.query(ModelCartProductDetail)\
                .filter_by(id=cart_product_detail_id)\
                .first()
            
            cart_product_detail_model.quantity = cart_product_detail.quantity
            cart_product_detail_model.price = cart_product_detail.price
            cart_product_detail_model.preference_product = cart_product_detail.preference_product
            cart_product_detail_model.retailer_id = cart_product_detail.retailer_id
            cart_product_detail_model.retailer_name = cart_product_detail.retailer_name
            
            
            self.db_session.add(cart_product_detail_model)

            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.log.info(f"update_cart done")
            return cart_product_detail_model           
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: setup_db.py method:, update_cart fail {e}")
            if raise_integrety_except:
                raise e
            raise None
