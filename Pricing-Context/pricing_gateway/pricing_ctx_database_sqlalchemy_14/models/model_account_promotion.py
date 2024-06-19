from typing import Any, Dict
from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from pricing_ctx_database_sqlalchemy_14.models.base import Base
from pricing_ctx_database_sqlalchemy_14.models.model_promotion import ModelPromotion


class ModelAccountPromotion(Base):

    """ModelAccountPromotion model."""

    __tablename__ = "Account_Promotion"

    id = Column(Integer, unique=True, primary_key=True,autoincrement=True, doc="Id of the account promotion")
    id_account_pricing = Column(Integer, ForeignKey('PricingAccount.id', ondelete='CASCADE'), primary_key=True, doc="Pricing Account Id")
    id_promotion = Column(Integer, ForeignKey('Promotion.id', ondelete='CASCADE'), primary_key=True, doc="Promotion Id")
    promotions_counter = Column(Integer, doc="How many times the promotion is applied", nullable=False, default=0)
    is_active= Column(Boolean, doc="If the promotion is active", nullable=False, default=True)
    created = Column(Integer, doc="Unix TimeStamp When the register is created", nullable=False, )
    updated = Column(Integer, doc="Unix TimeStamp When the register is updated", nullable=True, )


    promotion = relationship(
        ModelPromotion, lazy='subquery', backref="ModelAccountPromotion")
    

    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelAccountPromotion to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelAccountPromotion.__dict__.keys() }
