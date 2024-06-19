from typing import Any, Dict
from sqlalchemy import Column, Float, Integer, Date, SmallInteger, ForeignKey
from order_ctx_database_sqlalchemy_14.models.base import Base

class CartProductDetail(Base):
    """'CartProductDetail'model."""

    __tablename__ = "cart_product_detail"

    id = Column("ID", Integer, primary_key=True,autoincrement=True, doc="Id of the Cart Product")
    quantity = Column("Quantity", SmallInteger, doc="Quantity of the Cart Product")
    cost = Column("Cost", Float(10), doc="Cost of the Cart Product")
    price = Column("Price", Float(10), doc="Price of the Cart Product")
    product_added_date = Column("ProductAddedDate", Date(), doc="Added Date of the Cart Product")
    cart_id = Column('CartID', Integer, ForeignKey('cart.ID', ondelete='CASCADE'), doc="Foreign ID of the Cart")
    product_id = Column('ProductID', Integer, doc="Foreign ID of the Product")

    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy Cart to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in CartProductDetail.__dict__.keys()
        }