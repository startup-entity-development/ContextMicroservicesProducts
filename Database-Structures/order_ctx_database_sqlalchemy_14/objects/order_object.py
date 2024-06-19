
from typing import List
from order_ctx_database_sqlalchemy_14.models.order import Order
from order_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase
from order_ctx_database_sqlalchemy_14.models.base import db_session
from typing import Optional
from datetime import datetime

class OrderAttributesGateway(): 
    
    def __init__(self, **kwargs):
        self.address:str
        self.contact_number:str
        self.note:str
        self.product_delivery_date:str
        self.shopper_id:int
        self.cart_id:int
    
    @property
    def model_dictionary(self)->dict:
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in Order.__dict__.keys()
        }
    
    def from_dict(self, obj_dict:dict):
        self.__dict__.update(obj_dict)
        return self
    
class OrderDataBase(ObjectDataBase):
    def __init__(self, log):
        self.log = log
        self.db_session = db_session
        super().__init__(db_session, log)
        
    def create(self, order:OrderAttributesGateway, auto_commit:bool= True, raise_integrety_except=False) -> Optional[Order]:
        
        """Create order model."""
        try:
            order_dict = order.model_dictionary
            order_dict["address"] = order.address
            order_dict["contact_number"] = order.contact_number
            order_dict["note"] = order.note
            order_dict["created_date"] = datetime.now()
            order_dict["product_delivery_date"] = order.product_delivery_date
            order_dict["shopper_id"] = order.shopper_id
            order_dict["cart_id"] = order.cart_id
            
            order = Order(**order_dict)
            self.db_session.add(order)

            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.log.info(f"create_order done")
            return order  
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: setup_db.py method:, create_order fail {e}")
            if raise_integrety_except:
                raise e
            return None

    def delete_all(self, auto_commit:bool= True) -> None:
        """Delete all orders."""
        try:
            self.db_session.query(Order).delete()
            if auto_commit:
                self.db_session.commit()
            self.log.info(f"delete_all_orders done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, delete_all_orders fail {e}")        

    def get(self, id:int) -> Order:
        """Get order model."""
        try:
            order = self.db_session.query(Order).filter_by(id=id).first()
            self.log.info(f"get_order done")
            return order
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_order fail {e}")     
    
    def get_all(self) -> List[Order]:
        """Get all orders model."""
        try:
            orders = self.db_session.query(Order).all()
            self.log.info(f"get_all_orders done")
            return orders
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_all_orders fail {e}")
            
    
    def delete(self, id_order:int, auto_commit:bool= True):
        # delete order
        try:
            order = self.db_session.query(Order).get(id_order)
            self.db_session.delete(order)
            if auto_commit:
                self.db_session.commit()
            
            self.log.info(f"delete_order done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, delete_order fail {e}")


    def get_order_by_cart_id(self, cart_id:int) -> Order:
        """Get order model."""
        try:
            order = self.get_order_by_cart_id.query(Order).filter_by(cart_id=cart_id).first()
            self.log.info(f"get_order done")
            return order
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_order_by_cart_id fail {e}")     