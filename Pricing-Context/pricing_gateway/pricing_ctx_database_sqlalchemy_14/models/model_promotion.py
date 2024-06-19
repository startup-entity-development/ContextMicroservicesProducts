from typing import Any, Dict
from sqlalchemy import Column, String, Integer, Float, Enum, Boolean
from sqlalchemy.orm import relationship
from pricing_ctx_database_sqlalchemy_14.models.base import Base
from pricing_ctx_database_sqlalchemy_14.models.model_promotion_coupon import ModelPromotionCoupon


class ModelPromotion(Base):
    """Promotion model."""

    __tablename__ = "Promotion"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, doc="Id of the profile")
    promotion_name = Column(String(100), unique=True, nullable=False, doc="Name of the promotion")
    description = Column(String(500), unique=True, doc=" Description of the Promotion")
    value_percent = Column(Float, doc="Value percent", default=0)
    value_amount = Column(Float, doc="Value amount", default=0)
    minimum_threshold_subtotal = Column(Float, doc="Value threshold trigger subtotal", default=None, nullable=True)
    maximum_threshold_subtotal = Column(Float, doc="Value threshold trigger subtotal", default=None, nullable=True)
    minimum_threshold_delivery = Column(Float, doc="Minimum subtotal delivery", default=None, nullable=True)
    maximum_threshold_delivery = Column(Float, doc="Maximum subtotal delivery", default=None, nullable=True)
    minimum_threshold_service = Column(Float, doc="Minimum subtotal service", default=None, nullable=True)
    maximum_threshold_service = Column(Float, doc="Maximum subtotal service", default=None, nullable=True)
    minimum_threshold_quantity = Column(Integer, doc="Minimum quantity of products", default=None, nullable=True)
    type_promotion= Column(Enum('percent', 'amount', name= "type_promotion"), doc="Type of promotion", nullable=False,)
    where_applies = Column(Enum('product','product_category','product_subcategory', 'product_subtotal', 'delivery_fee', 'service_fee', name= "where_applies"), doc="Where the promotion applies the promotion", nullable=False, )
    times_of_use = Column(Integer, doc="How many times the promotion can be applied", nullable=False, default=1) 
    coupon_code = Column(String(64), unique=True, nullable=False, doc="Coupon code")
    rule_access_name = Column(String(100), unique=False, nullable=True, doc="Rule access")
    level_access_name = Column(String(100), unique=False, nullable=True, doc="Level access")
    start_timestamp = Column(Integer, doc="Unix Timestamp when the promotion starts", nullable=False, )
    end_timestamp = Column(Integer, doc="Unix Timestamp when the promotion ends", nullable=False)
    is_active = Column(Boolean, doc="If the promotion is active", nullable=False, default=True)
    created = Column(Integer, doc="Unix TimeStamp When the register is created", nullable=False )
    updated = Column(Integer, doc="Unix TimeStamp When the register is updated", nullable=True)
    
    promotion_coupon_edge = relationship(
        "ModelPromotionCoupon",
        backref="Promotion",
        viewonly=True,
        )
    
    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelPromotion to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelPromotion.__dict__.keys()
        }
