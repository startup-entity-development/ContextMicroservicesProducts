from typing import Any, Dict
from sqlalchemy import Column, String, Integer
from order_ctx_database_sqlalchemy_14.models.base import Base

class ModelStatus(Base):
    """'Status'model."""

    __tablename__ = "Status"

    id = Column(Integer, primary_key=True,autoincrement=True, doc="Id of the Status")
    name = Column( String(50), unique=False, doc="Name of the Status")

    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy Status to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelStatus.__dict__.keys()
        }