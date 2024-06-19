
from dataclasses import dataclass
import time
from typing import Any, Dict

from auth_model_sqlalchemy_14.role import ModelRole

@dataclass
class RoleAttribute():

    """
    RoleAttribute is a dataclass for role attributes
    """
    def __init__(self):
        self.role_name:str = None
        self.definition:str = None
        self.created:int = None
        self.edited:int = None
    
    def _format_attribute(self):
        """format attribute
        """
        now = int(time.time())
        if not self.created:
            self.created = now
        else:
            self.edited = now
    
    def _check_required_attribute(self):
        """check required attribute
        """
        if not self.role_name:
            raise Exception("Role_name is required")
        if not self.definition:
            raise Exception("Definition is required")
        
    
    def from_dict(self, data: Dict[str, Any]) :

        for field in [field for field in data if field in self.__dict__]:
            setattr(self, field, data[field])
        
        self._check_required_attribute()
        self._format_attribute()

        return self
    

 
    def to_dict(self) -> Dict[str, Any]:
        """ return a dict shallow copy AccountAttribute """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
        }
    
    def to_model_role(self) -> ModelRole:
        """ return a dict shallow copy AccountAttribute """
        obj_dict = self.__dict__.copy()
        return ModelRole(**{
            key: obj_dict.get(key)
            for key in obj_dict
        })
    


@dataclass
class LevelAttribute():
    """LevelAttribute is a dataclass for level attributes
    """
    def __init__(self):
        self.level_name:str = None
        self.level_value:int = None
        self.definition:str = None
        self.created:int = None
        self.edited:int = None
    
    def _format_attribute(self):
        """format attribute
        """
        now = int(time.time())
        if not self.created:
            self.created = now
        else:
            self.edited = now
    
    def _check_required_attribute(self):
        """check required attribute
        """
        if not self.level_name:
            raise Exception("Level_name is required")
        
        if not self.level_value:
            raise Exception("Level_value is required")
        
        if not self.definition:
            raise Exception("Definition is required")
        
    
    def from_dict(self, data: Dict[str, Any]) :
        for field in [field for field in data if field in self.__dict__]:
            setattr(self, field, data[field])
        
        self._check_required_attribute()
        self._format_attribute()

        return self
    

 
    def to_dict(self) -> Dict[str, Any]:
        """ return a dict shallow copy AccountAttribute """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
        }
    
@dataclass
class RoleLevelAttribute():
    """RoleLevelAttribute is a dataclass for role level attributes
    """
    def __init__(self):
        self.account_id:int = None
        self.role_id:int = None
        self.level_id:int = None
        self.is_active:bool = None
        self.created:int = None
        self.edited:int = None
    
    def _format_attribute(self):
        """format attribute
        """
        now = int(time.time())
        if not self.created:
            self.created = now
        else:
            self.edited = now
    
    def _check_required_attribute(self):
        """check required attribute
        """
        if not self.role_id:
            raise Exception("Role_id is required")
        if not self.level_id:
            raise Exception("Level_id is required")
        
    
    def from_dict(self, data: Dict[str, Any]) :

        for field in [field for field in data if field in self.__dict__]:
            setattr(self, field, data[field])
        
        self._check_required_attribute()
        self._format_attribute()

        return self
    

 
    def to_dict(self) -> Dict[str, Any]:
        """ return a dict shallow copy AccountAttribute """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
        }