
from typing import List
from order_ctx_database_sqlalchemy_14.models.cart import Cart
from order_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase
from order_ctx_database_sqlalchemy_14.models.base import db_session
from typing import Optional
from datetime import datetime
class CartAttributesGateway(): 
    
    def __init__(self, **kwargs):
        self.cart_total:float
        self.total:float
        self.delivery:str
        self.tax:float
        self.created_date:str
        self.deactive_date:str
    
    @property
    def model_dictionary(self)->dict:
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in Cart.__dict__.keys()
        }
    
    def from_dict(self, obj_dict:dict):
        self.__dict__.update(obj_dict)
        return self
    
class CartDataBase(ObjectDataBase):
    def __init__(self, log):
        self.log = log
        self.db_session = db_session
        super().__init__(db_session, log)
        
    def create(self, cart:CartAttributesGateway, auto_commit:bool= True, raise_integrety_except=False) -> Optional[Cart]:        
        """Create cart model."""
        try:
            cart_dict = cart.model_dictionary
            cart_dict["cart_total"] = cart.cart_total if hasattr(cart, "cart_total") else 0
            cart_dict["total"] = cart.total if hasattr(cart, "total") else 0
            cart_dict["delivery"] = cart.delivery if hasattr(cart, "delivery") else 0
            cart_dict["tax"] = cart.tax if hasattr(cart, "tax") else 0
            cart_dict["created_date"] = datetime.now()
            cart_dict["deactive_date"] = cart.deactive_date if hasattr(cart, "deactive_date") else None
            
            cart = Cart(**cart_dict)
            self.db_session.add(cart)

            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.log.info(f"create_cart done")
            return cart           
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: setup_db.py method:, create_cart fail {e}")
            if raise_integrety_except:
                raise e
            raise None

    def delete_all(self, auto_commit:bool= True) -> None:
        """Delete all carts."""
        try:
            self.db_session.query(Cart).delete()
            if auto_commit:
                self.db_session.commit()
            self.log.info(f"delete_all_carts done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, delete_all_carts fail {e}")        

    def get(self, id:int) -> Cart:
        """Get cart model."""
        try:
            cart = self.db_session.query(Cart).filter_by(id=id).first()
            self.log.info(f"get_cart done")
            return cart
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_cart fail {e}")     
    
    def get_all(self) -> List[Cart]:
        """Get all carts model."""
        try:
            carts = self.db_session.query(Cart).all()
            self.log.info(f"get_all_carts done")
            return carts
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_all_carts fail {e}")
            
    
    def delete(self, id_cart:int, auto_commit:bool= True):
        # delete cart
        try:
            cart = self.db_session.query(Cart).get(id_cart)
            self.db_session.delete(cart)
            if auto_commit:
                self.db_session.commit()
            
            self.log.info(f"delete_cart done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, delete_cart fail {e}")
