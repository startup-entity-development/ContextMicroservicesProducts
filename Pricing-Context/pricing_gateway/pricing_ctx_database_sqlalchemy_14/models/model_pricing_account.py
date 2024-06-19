from typing import Any, Dict
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pricing_ctx_database_sqlalchemy_14.models.base import Base
from pricing_ctx_database_sqlalchemy_14.models.model_pricing_profile import ModelPricingProfile
from pricing_ctx_database_sqlalchemy_14.models.model_account_promotion import ModelAccountPromotion


class ModelPricingAccount(Base):
    """
    ModelPricingAccount model.
    Child of PricingProfile
    """
    
    __tablename__ = "PricingAccount"

    id = Column(Integer, unique=True, primary_key=True,autoincrement=True, doc="Id of the SubCategory")
    external_account_id = Column(String(100), unique=True, nullable=False, doc="External Account Id")
    pricing_profile_id = Column(Integer, ForeignKey('PricingProfile.id',ondelete='CASCADE'), doc="Pricing Profile Id")
    created = Column(Integer, doc="When the register is created", nullable=False )
    updated = Column(Integer, doc="When the register is updated", nullable=True)
    
    pricing_profile = relationship(ModelPricingProfile, back_populates="pricing_account_edge")

    account_promotion_edge = relationship(
        ModelAccountPromotion,
        backref="PricingAccount")
    
    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelPricingAccount to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelPricingAccount.__dict__.keys()
        }
