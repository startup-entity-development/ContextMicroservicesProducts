from typing import Any, Dict
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from product_ctx_database_sqlalchemy_14.models.base import Base

class ModelMedia(Base):
    """'Media'model."""

    __tablename__ = "Media"

    id = Column(Integer, primary_key=True, autoincrement=True, doc="Id of the Media")
    media_type = Column(String(50), doc="Type of the Media")
    product_id = Column(ForeignKey('Product.id', ondelete='CASCADE'), doc="Foreign ID of the Product", primary_key=True)
    name = Column(String(50), doc="Name of the Media")
    description = Column(String(255), unique=False, doc=" Description of the Media")
    link_url = Column(String(250), unique=False, doc="LinkUrl of the Media")
    is_main = Column(Boolean, nullable=False, doc="True if the Media is main, example: Main image of the product")

    
    

    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelMedia to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelMedia.__dict__.keys()
        }