from typing import Any, Dict
from sqlalchemy import Column, Float, Integer, Date
from order_ctx_database_sqlalchemy_14.models.base import Base

class Cart(Base):
    """'Cart'model."""

    __tablename__ = "cart"

    id = Column("ID", Integer, primary_key=True,autoincrement=True, doc="Id of the Cart")
    cart_total = Column("CartTotal", Float(10), doc="Cart total of the Cart")
    total = Column("Total", Float(10), doc="Total of the Cart")
    delivery = Column("Delivery", Float(10), doc="Delivery of the Cart")
    tax = Column("Tax", Float(10), doc="Tax of the Cart")
    created_date = Column("CreatedDate", Date(), doc="Created Date of the Cart")
    deactive_date = Column("DeactiveDate", Date(), doc="DeActive Date of the Cart")
    

    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy Cart to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in Cart.__dict__.keys()
        }