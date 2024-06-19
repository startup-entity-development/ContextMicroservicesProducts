from typing import Any, Dict
from sqlalchemy import Column, Float, Integer, Date, String
from order_ctx_database_sqlalchemy_14.models.base import Base

class ModelCustomer(Base):
    """'Customer'model."""

    __tablename__ = "Customer"

    id = Column( Integer, primary_key=True,autoincrement=True, doc="Id of the Customer")
    name = Column( String(50), unique=False, doc="Name of the Customer")
    stripe_customer_id = Column( String(100), unique=True, doc="Unique stripe customer id")

    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy Customer to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelCustomer.__dict__.keys()
        }