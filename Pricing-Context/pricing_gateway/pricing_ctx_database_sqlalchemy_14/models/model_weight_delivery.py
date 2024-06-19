from typing import Any, Dict
from sqlalchemy import Column, String, Integer, Float
from pricing_ctx_database_sqlalchemy_14.models.base import Base


class ModelWeightDelivery(Base):
    """WeightDelivery model."""

    __tablename__ = "WeightDelivery"

    id = Column(Integer, unique=True, primary_key=True,autoincrement=True, doc="Id of the profile weight delivery")
    name = Column(String(100), unique=True, nullable=False, doc="Name of the profile weight delivery")
    delivery_threshold_pound = Column(Float, doc="Extra Delivery Increment of the profile ", default=1)
    price_delivery = Column(Float, doc="Price of delivery", default=0)
    created = Column(Integer, doc="Unix TimeStamp When the register is created", nullable=False, )
    updated = Column(Integer, doc="Unix TimeStamp When the register is updated", nullable=True, )
    
    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelSubCategory to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelWeightDelivery.__dict__.keys()
        }
