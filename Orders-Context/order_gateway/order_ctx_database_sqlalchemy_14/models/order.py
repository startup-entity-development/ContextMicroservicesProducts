from typing import Any, Dict
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from order_ctx_database_sqlalchemy_14.models.base import Base
from order_ctx_database_sqlalchemy_14.models.cart import ModelCart
from sqlalchemy.orm import relationship

class ModelOrder(Base):
    """'Order'model."""

    __tablename__ = "Order"

    id = Column(Integer, primary_key=True,autoincrement=True, doc="Id of the Order")
    address = Column( String(150), unique=False, doc="Address of the Customer")
    contact_number = Column( String(15), unique=False, doc="Contact Number of the Customer")
    note = Column(String(255), unique=False, doc="Note of the Customer")
    created_date = Column(Date(), doc="Created Date of the Order")
    product_delivery_date = Column( Date(), doc="Product Delivery Date of the Order")
    shopper_id = Column( Integer, ForeignKey('Shopper.id', ondelete='CASCADE'), doc="Foreign ID of the Shopper")
    cart_id = Column( Integer, ForeignKey('Cart.id', ondelete='CASCADE'), doc="Foreign ID of the Cart")
    user_account_id = Column( Integer, doc="Account id of the related user")
    
    cart = relationship(ModelCart, uselist=False)

    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy Order to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelOrder.__dict__.keys()
        }