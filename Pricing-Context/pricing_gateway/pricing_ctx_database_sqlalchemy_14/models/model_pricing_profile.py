from typing import Any, Dict
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from pricing_ctx_database_sqlalchemy_14.models.base import Base


class ModelPricingProfile(Base):
    """PricingProfile model."""

    __tablename__ = "PricingProfile"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, doc="Id of the profile")
    name_profile = Column(String(100), unique=True, nullable=False, doc="Name of the profile")
    tax = Column(Float, doc="Tax", default=0)
    delivery_fee_base = Column(Float, doc="Base Delivery Fee", default=0)
    service_fee_base = Column(Float, doc="Base Service Fee", default=0)
    minimum_subtotal = Column(Float, doc="Minimum amount product subtotal", default=30)
    rule_access_name = Column(String(100), unique=False, nullable=True, doc="Rule access")
    level_access_name = Column(String(100), unique=False, nullable=True, doc="Level access",)
    priority = Column(Float, doc="Priority value used for determining the order of profiles", unique=True, default=0, nullable=False)
    description = Column(String(255), unique=True, doc=" Description of the Profile")
    created = Column(Integer, doc="Unix TimeStamp When the register is created", nullable=False )
    edited = Column(Integer, doc="Unix TimeStamp When the register is edited", nullable=True, )

    pricing_account_edge = relationship(
        "ModelPricingAccount",
        backref="PricingProfile",
        viewonly=True,
        )


    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy PricingProfile to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelPricingProfile.__dict__.keys()
        }
