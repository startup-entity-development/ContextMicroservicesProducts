from typing import Any, Dict
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from auth_model_sqlalchemy_14_pha.base import Base
from auth_model_sqlalchemy_14_pha.location import ModelLocation

class ModelPerson(Base):
    """Person model."""

    __tablename__ = "Person"

    
    id = Column(Integer, primary_key=True, doc="Id of the RoleLevel ")
    account_id = Column(ForeignKey('Account.id', ondelete='CASCADE'), doc="Foreign ID of the Account")
    name = Column(String(250), unique=False, doc="Person Name")
    surname = Column(String(250), unique=False, doc="Person Surname")
    phone_number = Column(String(250), unique=True, doc="Person Phone Number")
    created = Column(Integer, doc="Record the creation timestamp of the current entry using a base-10 timestamp")
    edited = Column(Integer, doc="Record the update timestamp of the current entry using a base-10 timestamp")
    location_List = relationship(ModelLocation, passive_deletes=True, backref="Person")

    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelPerson to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelPerson.__dict__.keys()
        }
