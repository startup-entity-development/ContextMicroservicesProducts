from typing import Any, Dict
from sqlalchemy import Column, String, Integer
from order_ctx_database_sqlalchemy_14.models.base import Base

class Shopper(Base):
    """'Shopper'model."""

    __tablename__ = "shopper"

    id = Column("ID", Integer, primary_key=True,autoincrement=True, doc="Id of the Shopper")
    name = Column("Name", String(50), unique=False, doc="Name of the Shopper")

    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy Shopper to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in Shopper.__dict__.keys()
        }