from typing import Any, Dict
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from order_ctx_database_sqlalchemy_14.models.base import Base

class Order(Base):
    """'Order'model."""

    __tablename__ = "order"

    id = Column("ID", Integer, primary_key=True,autoincrement=True, doc="Id of the Order")
    address = Column("Address", String(150), unique=False, doc="Address of the Customer")
    contact_number = Column("ContactNumber", String(15), unique=False, doc="Contact Number of the Customer")
    note = Column("Note", String(255), unique=False, doc="Note of the Customer")
    created_date = Column("CreatedDate", Date(), doc="Created Date of the Order")
    product_delivery_date = Column("ProductDeliveryDate", Date(), doc="Product Delivery Date of the Order")
    shopper_id = Column('ShopperID', Integer, ForeignKey('shopper.ID', ondelete='CASCADE'), doc="Foreign ID of the Shopper")
    cart_id = Column('CartID', Integer, ForeignKey('cart.ID', ondelete='CASCADE'), doc="Foreign ID of the Cart")

    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy Order to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in Order.__dict__.keys()
        }