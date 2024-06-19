from typing import Any, Dict
from sqlalchemy import Column, Float, Integer, Date
from sqlalchemy.orm import relationship
from order_ctx_database_sqlalchemy_14.models.base import Base


class ModelCart(Base):
    """'Cart'model."""

    __tablename__ = "Cart"

    id = Column(Integer, primary_key=True,autoincrement=True, doc="Id of the Cart")
    created_date = Column( Date(), doc="Created Date of the Cart")
    deactive_date = Column( Date(), doc="DeActive Date of the Cart")
    user_account_id = Column( Integer, doc="Account id of the related user")

    #cart_products_edge = relationship(ModelCartProductDetail)
    cart_products_edge = relationship(
        "ModelCartProductDetail",
        viewonly=True,
        backref="Cart")
    

    

    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy Cart to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelCart.__dict__.keys()
        }

    def calculate_sub_total(self) -> float:
        total = 0
        for product in self.cart_products_edge:
            total += product.price * product.quantity
        return total
