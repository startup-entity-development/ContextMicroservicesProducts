from typing import Any, Dict
from sqlalchemy import Column, String, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from product_ctx_database_sqlalchemy_14.models.base import Base
from product_ctx_database_sqlalchemy_14.models.product_model import ModelProduct


class ModelSubCategory(Base):
    """SubCategory model."""

    __tablename__ = "SubCategory"

    id = Column(Integer, unique=True, primary_key=True,autoincrement=True, doc="Id of the SubCategory")
    api_id = Column(String(100), unique=True, nullable=False, doc="ApiID of the Product")
    category_id = Column( ForeignKey('Category.id', ondelete='CASCADE'), doc="Foreign ID Id of the Category", primary_key=True)
    image = Column(String(255), unique=False, doc="Image of the SubCategory")
    name = Column( String(100), unique=True, doc="Name of the SubCategory")
    default_base_increment = Column(Float, doc="Default Base Increment of the SubCategory", default=1)
    description = Column(String(255), unique=False, doc=" Description of the SubCategory")
    
    product_edge = relationship(
        ModelProduct,
        passive_deletes=True,
        cascade="all, delete-orphan",
        backref="SubCategory")
    
    
    
    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelSubCategory to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelSubCategory.__dict__.keys()
        }
