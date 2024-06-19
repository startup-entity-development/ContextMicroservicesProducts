from typing import Any, Dict
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Boolean
from sqlalchemy.orm import relationship
from product_ctx_database_sqlalchemy_14.models.base import Base
from product_ctx_database_sqlalchemy_14.models.retailer_model import ModelRetailer

class ModelProductRetailer(Base):
    """ProductRetailer model."""

    __tablename__ = "Product_Retailer"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, doc="Id of the ProductRetailer")
    retailer_id = Column(ForeignKey('Retailer.id', ondelete='CASCADE'), nullable=False, doc="Foreign ID Id of the Retailer")
    product_id = Column( ForeignKey('Product.id', ondelete='CASCADE'), nullable=False, 
                        doc="Foreign ID of the Product and unique")
    link_url = Column( String(250), unique=True, doc="LinkUrl of the Product")
    cost = Column(Float(10), nullable=True, doc="Cost of the Product")
    increment_retailer = Column(Float, doc="Increment based in the retailer", default=1)
    stock = Column(Integer, doc="Stock of the Product", nullable=True)
    is_active = Column(Boolean, doc="Status of the Product", nullable=True)
    is_in_stock = Column(Boolean, doc="Status of the Product", nullable=True, default=True)
    
    retailer = relationship(
        ModelRetailer,  backref="Product_Retailer",overlaps="Product_Retailer,retailer", viewonly=True)
    
    product = relationship(
        "ModelProduct",  backref="Product_Retailer",overlaps="Product_Retailer,product", viewonly=True)
    
    
    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelProductRetailer to dict """
        
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelProductRetailer.__dict__.keys()
        }