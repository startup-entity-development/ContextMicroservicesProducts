from typing import Any, Dict
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship

from product_ctx_database_sqlalchemy_14.models.base import Base

class ModelRetailer(Base):
    """Retailer model."""

    __tablename__ = "Retailer"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, doc="Id of the Retailer")
    name = Column(String(50), unique=True, doc="Name of the Retailer")
    description = Column( String(255), unique=False, doc=" Description of the Retailer")
    
    
    product_retailer_edge = relationship(
        "ModelProductRetailer",
        passive_deletes=True,
        cascade="all, delete-orphan",
        backref="Retailer")

    
    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelRetailer to dict """
        obj_dict = self.__dict__.copy()
        return {
             key: obj_dict.get(key)
             for key in obj_dict
             if key in ModelRetailer.__dict__.keys()
         }