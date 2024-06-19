from typing import Any, Dict
from sqlalchemy import Column, Float, Integer, Date, SmallInteger, ForeignKey, String
from order_ctx_database_sqlalchemy_14.models.base import Base
from order_ctx_database_sqlalchemy_14.models.cart import ModelCart
from sqlalchemy.orm import relationship

class ModelCartProductDetail(Base):
    """'CartProductDetail'model."""

    __tablename__ = "CartProductDetail"

    id = Column( Integer, primary_key=True,autoincrement=True, doc="Id of the Cart Product")
    quantity = Column( SmallInteger, doc="Quantity of the Cart Product")
    price = Column( Float, doc="Price of the Cart Product")
    product_added_date = Column( Date(), doc="Added Date of the Cart Product")
    cart_id = Column(Integer, ForeignKey('Cart.id', ondelete='CASCADE'), doc="Foreign ID of the Cart")
    product_id = Column( Integer, doc="Foreign ID of the Product")
    retailer_id = Column(String(100), doc="Foreign ID of the Retailer", nullable=False)
    retailer_name = Column( String(100), doc="Foreign ID of the Retailer", nullable=True)
    preference_product = Column( String(250), doc="Note of the Product", nullable=True)

    cart = relationship(ModelCart, back_populates="cart_products_edge")
    
    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy Cart to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelCartProductDetail.__dict__.keys()
        }