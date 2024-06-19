from typing import Any, Dict
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship

from product_ctx_database_sqlalchemy_14.models.base import Base


class ModelCategory(Base):
    """Category model."""

    __tablename__ = "Category"

    id = Column(Integer, unique=True, primary_key=True,autoincrement=True, doc="Id of the Category")
    api_id = Column(String(100), unique=True, nullable=False, doc="ApiID of the Product")
    name = Column(String(100), unique=True, doc="External ID of the Category")
    default_base_increment = Column(Float, doc="Default Base Increment of the Category", default=1)
    description = Column(String(255), unique=True, doc=" Description of the Category")
    
    
    sub_category_edge = relationship(
        "ModelSubCategory",
        passive_deletes=True,
        cascade="all, delete-orphan",
        backref="Category")
    
    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelSubCategory to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelCategory.__dict__.keys()
        }
