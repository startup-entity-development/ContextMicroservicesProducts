from typing import Any, Dict
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from auth_model_sqlalchemy_14.base import Base
from auth_model_sqlalchemy_14.role import ModelRole
from auth_model_sqlalchemy_14.person import ModelPerson

class ModelAccount(Base):
    """Account model."""

    __tablename__ = "Account"

    id = Column(Integer, primary_key=True, doc="Id of the account")
    external_id = Column(String(64), unique=True, doc="External ID of the account ")
    user_name = Column(String(64), unique=True, doc="Id_name of the account ")
    password = Column(String(256), nullable=False, doc="Password of the account.")
    email = Column(String(256), nullable=False, unique=True, doc="Email of the account.")
    is_verified = Column(Boolean, default=0, nullable=False, doc="True if the account is verified, example: Email verification")
    is_active = Column(Boolean, default=1, nullable=False, doc="True if the account is active, default True")
    is_soft_deleted = Column(Boolean, default=0, nullable=False, doc="True if the account are soft deleted")
    delete_reason = Column(String(256), doc="Reason for soft delete")
    created = Column(Integer, doc="Record the creation timestamp of the current entry using a base-10 timestamp")
    edited = Column(Integer, doc="Record the update timestamp of the current entry using a base-10 timestamp")
    person = relationship("ModelPerson", backref="Account")
    role_level_List = relationship("ModelAccountRoleLevel",  backref="Account")
    
    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelAccount to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelAccount.__dict__.keys()
        }

