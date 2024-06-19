from typing import Any, Dict
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from auth_model_sqlalchemy_14_pha.base import Base


class ModelRole(Base):
    """Role model."""

    __tablename__ = "Role"

    id = Column(Integer, primary_key=True, doc="Id of the Role ")
    role_name = Column(String(100), unique=True, doc="Role Name")
    definition = Column(String(1500), unique=False, doc="Definition of the Role")
    created = Column(Integer, doc="Record the creation timestamp of the current entry using a base-10 timestamp")
    edited = Column(Integer, doc="Record the update timestamp of the current entry using a base-10 timestamp")
    
    
    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelRole to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelRole.__dict__.keys()
        }

