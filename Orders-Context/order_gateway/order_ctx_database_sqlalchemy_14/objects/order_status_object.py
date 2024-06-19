
import logging
from typing import List
from order_ctx_database_sqlalchemy_14.models.order_status import ModelOrderStatus
from order_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase

class OrderStatusDataBase(ObjectDataBase):
    def __init__(self, db_session, log):
        super().__init__(db_session, log)
        
    def create(
            self,
            start_date: str,
            end_date: str,
            order_id: int,
            status_id: int,
            auto_commit:bool=True
        ) -> ModelOrderStatus:
        
        """Create order_status model."""
        try:
            order_status = ModelOrderStatus(
                start_date=start_date,
                end_date=end_date,
                order_id=order_id,
                status_id=status_id,
            )
            self.db_session.add(order_status)
            if auto_commit: 
                self.db_session.commit()
            else:
                self.db_session.flush()
                
            self.log.info(f"create_order_status done")
            return order_status
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, create_order_status fail {e}")

    def delete_all(self, auto_commit:bool= True) -> None:
        """Delete all order_statuss."""
        try:
            self.db_session.query(ModelOrderStatus).delete()
            if auto_commit:
                self.db_session.commit()
            self.log.info(f"delete_all_order_statuss done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, delete_all_order_statuss fail {e}")        

    def get(self, id:int) -> ModelOrderStatus:
        """Get order_status model."""
        try:
            order_status = self.db_session.query(ModelOrderStatus).filter_by(id=id).first()
            self.log.info(f"get_order_status done")
            return order_status
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_order_status fail {e}")     
    
    def get_all(self) -> List[ModelOrderStatus]:
        """Get all order_statuss model."""
        try:
            order_statuss = self.db_session.query(ModelOrderStatus).all()
            self.log.info(f"get_all_order_statuss done")
            return order_statuss
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, get_all_order_statuss fail {e}")
            
    
    def delete(self, id_order_status:int, auto_commit:bool= True):
        # delete order_status
        try:
            order_status = self.db_session.query(ModelOrderStatus).get(id_order_status)
            self.db_session.delete(order_status)
            if auto_commit:
                self.db_session.commit()
            
            self.log.info(f"delete_order_status done")
        except Exception as e:
            self.log.error(f"file: setup_db.py method:, delete_order_status fail {e}")
