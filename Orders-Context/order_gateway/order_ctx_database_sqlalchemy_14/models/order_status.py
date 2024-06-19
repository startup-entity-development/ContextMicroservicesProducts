from typing import Any, Dict
from sqlalchemy import Column, ForeignKey, Integer, Date
from order_ctx_database_sqlalchemy_14.models.base import Base

class ModelOrderStatus(Base):
    """'OrderStatus'model."""

    __tablename__ = "OrderStatus"

    id = Column(Integer, primary_key=True,autoincrement=True, doc="Id of the Customer")
    start_date = Column( Date(), doc="Start Date of the OrderStatus")
    end_date = Column( Date(), doc="End Date of the Cart")
    order_id = Column( Integer, ForeignKey('Order.id', ondelete='CASCADE'), doc="Foreign ID of the Order")
    status_id = Column( Integer, ForeignKey('Status.id', ondelete='CASCADE'), doc="Foreign ID of the Status")

    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy OrderStatus to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelOrderStatus.__dict__.keys()
        }