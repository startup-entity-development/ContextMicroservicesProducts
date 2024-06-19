from typing import Any, Dict
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from auth_model_sqlalchemy_14.base import Base


class ModelLevel(Base):
    """Level model."""

    __tablename__ = "Level"

    id = Column(Integer, primary_key=True, doc="Id of the Level ")
    level_name = Column(String(100), unique=True, doc="Level name")
    level_value = Column(Integer, unique=True, doc="Level value", default=0, nullable=False)
    definition = Column(String(1500), unique=False, doc="Definition of the level")
    created = Column(Integer, doc="Record the creation timestamp of the current entry using a base-10 timestamp")
    edited = Column(Integer, doc="Record the update timestamp of the current entry using a base-10 timestamp")

    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelLevel to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelLevel.__dict__.keys()
        }
