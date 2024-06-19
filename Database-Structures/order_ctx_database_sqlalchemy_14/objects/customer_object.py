
from typing import List
from order_ctx_database_sqlalchemy_14.models.customer import Customer
from order_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase
from order_ctx_database_sqlalchemy_14.models.base import db_session
from typing import Optional
class CustomerAttributesGateway(): 
    
    def __init__(self, **kwargs):
        self.name:str
        self.stripe_customer_id:str
    
    @property
    def model_dictionary(self)->dict:
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in Customer.__dict__.keys()
        }
    
    def from_dict(self, obj_dict:dict):
        self.__dict__.update(obj_dict)
        return self
    
class CustomerDataBase(ObjectDataBase):
    def __init__(self, log):
        self.log = log
        self.db_session = db_session
        super().__init__(db_session, log)
        
    def create(self, customer:CustomerAttributesGateway, auto_commit:bool= True, raise_integrety_except=False) -> Optional[Customer]:
        """Create customer."""
        try:
            customer_dict = customer.model_dictionary   
            customer_dict["name"] = customer.name
            
            customer = Customer(**customer_dict)
            self.db_session.add(customer)

            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.log.info(f"create_customer done")
            return customer           
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: setup_db.py method:, create_customer fail {e}")
            if raise_integrety_except:
                raise e
            raise None

    def delete_all(self, auto_commit:bool= True) -> None:
        """Delete all customers."""
        try:
            self.db_session.query(Customer).delete()
            if auto_commit:
                self.db_session.commit()
            self.log.info(f"delete_all_customers done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, delete_all_customers fail {e}")        

    def get(self, id:int) -> Customer:
        """Get customer model."""
        try:
            customer = self.db_session.query(Customer).filter_by(id=id).first()
            self.log.info(f"get_customer done")
            return customer
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_customer fail {e}")     
    
    def get_all(self) -> List[Customer]:
        """Get all customers model."""
        try:
            customers = self.db_session.query(Customer).all()
            self.log.info(f"get_all_customers done")
            return customers
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_all_customers fail {e}")
            
    
    def delete(self, id_customer:int, auto_commit:bool= True):
        # delete customer
        try:
            customer = self.db_session.query(Customer).get(id_customer)
            self.db_session.delete(Customer)
            if auto_commit:
                self.db_session.commit()
            
            self.log.info(f"delete_customer done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, delete_customer fail {e}")
