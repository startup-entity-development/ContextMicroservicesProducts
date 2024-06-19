from typing import Dict, Any
from auth_model_sqlalchemy_14_pha.base import Base
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from auth_model_sqlalchemy_14_pha.role import ModelRole

class ModelAccountRoleLevel(Base):
    """Many to Many model Account_Role_Level"""
    __tablename__ = 'Account_Role_Level'
    id = Column(Integer, primary_key=True, autoincrement=True, doc="Id of the RoleLevel ")
    account_id = Column(ForeignKey('Account.id', ondelete='CASCADE'), doc="Foreign ID of the Account", primary_key=True)
    role_id = Column(ForeignKey('Role.id', ondelete='CASCADE'), doc="Foreign ID Id of the role", primary_key=True)
    level_id = Column(ForeignKey('Level.id', ondelete='CASCADE'), doc="Foreign ID of the level", primary_key=True)
    is_active = Column(Boolean, default=0, nullable=False, doc="True if the account role is active, default False")
    created = Column(Integer, doc="Record the creation timestamp of the current entry using a base-10 timestamp")
    edited = Column(Integer, doc="Record the update timestamp of the current entry using a base-10 timestamp")
    role = relationship(ModelRole,
                        lazy='subquery',
                         backref="Account_Role_Level")
    level = relationship("ModelLevel",
                         lazy='subquery',
                           backref="Account_Role_Level")
    
    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelAccountRoleLevel to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelAccountRoleLevel.__dict__.keys()
        }

