from typing import Any, Dict
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Boolean
from sqlalchemy.orm import relationship
from product_ctx_database_sqlalchemy_14.models.base import Base

class ModelRetailerLocation(Base):
    """ Retailer Location model."""

    __tablename__ = "RetailerLocation"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, doc="Id of the Retailer Location")
    retailer_id = Column( ForeignKey('Retailer.id', ondelete='CASCADE'), doc="Foreign ID Id of the Retailer", primary_key=True)
    street_addr = Column(String(100), unique=False, doc="Street Address of the Retailer")
    city = Column( String(50), unique=False, doc=" City of the Retailer")
    state = Column(String(2), unique=False, doc="State of the Retailer")
    zipcode = Column(String(5), unique=False, doc="Zip Code of the Retailer")
    country = Column(String(10), unique=False, doc="Country of the Retailer")
    latitude = Column(Float, unique=False, doc="Latitude of the Retailer")
    longitude = Column(Float, unique=False, doc="Longitude of the Retailer")
    is_active = Column(Boolean, unique=False, doc="Is Active of the Retailer",default=True )
    created= Column(Integer, unique=False, doc="Created of the Retailer", nullable=True, default=0)
    updated = Column(Integer, unique=False, doc="Updated of the Retailer", nullable=True)

    retailer = relationship("ModelRetailer", back_populates="location_retailer_edge", viewonly=True, lazy='joined')

    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelRetailerLocation to dict """
        obj_dict = self.__dict__.copy()
        return {
             key: obj_dict.get(key)
             for key in obj_dict
             if key in ModelRetailerLocation.__dict__.keys()
         }