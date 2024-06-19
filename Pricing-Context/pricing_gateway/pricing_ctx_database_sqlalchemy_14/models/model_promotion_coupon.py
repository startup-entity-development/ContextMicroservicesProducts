from re import sub
from typing import Any, Dict
from sqlalchemy import Column, String, Integer, ForeignKey,Enum, Boolean
from pricing_ctx_database_sqlalchemy_14.models.base import Base
from sqlalchemy.orm import relationship


class ModelPromotionCoupon(Base):
    """Promotion Coupon"""

    __tablename__ = "PromotionCoupon"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, doc="Id of the promotion label")
    id_promotion = Column(Integer, ForeignKey('Promotion.id', ondelete='CASCADE'), doc="Promotion Id")
    language = Column(Enum('en', 'es', name= "language"), doc="Language of the label", nullable=False, default='en')
    title = Column(String(100), unique=True, nullable=False, doc="Title of the promotion")
    title_font_size = Column(Integer, doc="Font size of the title", nullable=False, default=16)
    subtitle = Column(String(100), unique=True, doc="Subtitle of the Promotion")
    sub_title_font_size = Column(Integer, doc="Font size of the subtitle", nullable=False, default=14)
    description = Column(String(300), unique=True, doc=" Description of the Promotion")
    description_font_size = Column(Integer, doc="Font size of the description", nullable=False, default=12)
    footer_1 = Column(String(100), unique=True, doc="Footer of the Promotion")
    footer_1_font_size = Column(Integer, doc="Font size of the footer", nullable=False, default=12)
    footer_2 = Column(String(100), unique=True, doc="Footer of the Promotion")
    footer_2_font_size = Column(Integer, doc="Font size of the footer", nullable=False, default=12)
    image = Column(String(250), unique=True, doc="Image of the Promotion")
    image_width = Column(Integer, doc="Width of the image", nullable=False, default=100)
    active = Column(Boolean, doc="If the promotion label is active", nullable=False, default=True)
    created = Column(Integer, doc="Unix TimeStamp When the register is created", nullable=False)
    updated = Column(Integer, doc="Unix TimeStamp When the register is updated", nullable=True)
    
    promotion = relationship(
        "ModelPromotion",
        backref="PromotionCoupon")
    
        
    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelPromotion to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelPromotionCoupon.__dict__.keys()
        }
