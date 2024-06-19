from typing import Any, Dict
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from auth_model_sqlalchemy_14.base import Base


class ModelLocation(Base):
    """Location model."""

    __tablename__ = "Location"

    id = Column(Integer, primary_key=True, doc="Id of the Location")
    person_id = Column(ForeignKey("Person.id", ondelete="CASCADE"), doc="Id of the Person")
    address = Column(String(255), unique=False, doc="Location address")
    zipcode = Column(String(10), unique=False, doc="Location zipcode")
    city = Column(String(50), unique=False, doc="City")
    map_address = Column(String(500), unique=False, doc="Map address")    
    created = Column(Integer, doc="Record the creation timestamp of the current entry using a base-10 timestamp")
    edited = Column(Integer, doc="Record the update timestamp of the current entry using a base-10 timestamp")
    
    
    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelLocation to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelLocation.__dict__.keys()
        }
