from __future__ import annotations
from dataclasses import dataclass
import hashlib
import os
import time
from typing import Any, Dict
from utils import remove_symbols_white_to_lower

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

@dataclass
class AccountAttribute():

    def __init__(self,
                    external_id:str=None,
                    user_name:str=None,
                    password:str=None,
                    email:str=None,
                    is_verified:bool=False,
                    is_active:bool=True,
                    is_soft_deleted:bool=False,
                    created:int=None,
                    edited:int=None ):
        
        self.external_id:str =  external_id # limit 16 characters, only letters and numbers
        self.user_name:str = user_name # limit 16 characters, only letters and numbers
        self.password:str = password
        self.email:str = email 
        self.is_verified:bool = is_verified
        self.is_active:bool = is_active
        self.is_soft_deleted:bool = is_soft_deleted
        self.created:int = created
        self.edited:int = edited

    def check_format_password(self):
            """Checks the format of the password.
            """
            len_password = len(self.password)

            if isinstance(self.password, str) == False:
                raise Exception("password must be a string, not a {}".format(type(self.password)))
            if len_password < 7:
                raise Exception("The minimum required password length is 7")
            if len_password > 16:
                raise Exception("The maximum required password length is 16")
            # check space in password
            if " " in self.password:
                raise Exception("The password cannot contain spaces")
    
                
    def get_encode_password(self) -> str:
        """ return password encoded whit a secret key """
        to_encode = f"{self.password}&{JWT_SECRET_KEY}"
        # Warning if to_encode key is changed, the password will be changed 
        #so the user will have to reset the password
        return hashlib.md5(to_encode.encode("utf-8")).hexdigest()

    def _format_attribute(self):
        """
        Formats the account attribute by performing the following actions:
        - Converts the email to lowercase.
        - Encodes the password.
        - Sets the created or edited timestamp.
        - Converts the username to lowercase and removes symbols.

        Returns:
        None
        """
        now = int(time.time()) 
        self.email = self.email.lower()
        self.password = self.get_encode_password()
        if not self.created:
            self.created = now
        else:
            self.edited = now

        if self.user_name:
            self.user_name = self.user_name.lower()
            self.user_name = remove_symbols_white_to_lower(self.user_name)
            

    def _check_required_attribute(self):

        if not self.email:
            raise Exception("Email is required")
        self.check_format_password()
            
    
    def from_dict(self, data: Dict[str, Any]) -> AccountAttribute:
            """
            Populates the AccountAttribute object from a dictionary.

            Args:
                data (Dict[str, Any]): The dictionary containing the attribute data.

            Returns:
                AccountAttribute: The populated AccountAttribute object.
            """

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
class PersonAttribute():
    def __init__(self):
        self.account_id:int = None
        self.name:str = None
        self.surname:str = None
        self.phone_number:str = None
        self.created:int = None
        self.edited:int = None
    
    def _check_required_attribute(self):

        if not self.name:
            raise Exception("Name is required")
        if not self.surname:
            raise Exception("Surname is required")
        if not self.phone_number:
            raise Exception("Phone_number is required")

    
    def _format_attribute(self):
    
        now = int(time.time()) 
        if not self.created:
            self.created = now
        else:
            self.edited = now

   

    def from_dict(self, data: Dict[str, Any]) -> PersonAttribute:
        

        for field in [field for field in data if field in self.__dict__]:
            setattr(self, field, data[field])
        
        self._check_required_attribute()
        self._format_attribute()
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
        }

@dataclass
class LocationAttribute():

    def __init__(self):
        self.person_id:int = None
        self.address:str = None
        self.zipcode:str = None
        self.city:str = None
        self.map_address:str = None
        self.created:int = None
        self.edited:int = None

    def _check_required_attribute(self):
        if not self.address:
            raise Exception("address is required")
        if not self.city:
            raise Exception("city is required")
       

    def from_dict(self, data: Dict[str, Any]) -> LocationAttribute:
        """ set attribute from dict"""

        for field in [field for field in data if field in self.__dict__]:
            setattr(self, field, data[field])
        if self.created is None:
            self.created = int(time.time())
        else:
            self.edited = int(time.time())
            
        self._check_required_attribute()

        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """return  shallow copy ModelAccount to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            }
        
        
@dataclass
class AccountRoleLevelAttribute():

    def __init__(self):
        self.account_id:int = None
        self.role_id:int = None
        self.level_id:int = None
        self.is_active:bool = True
        self.created:int = None
        self.edited:int = None  
        
    def to_dict(self) -> Dict[str, Any]:
        """return  shallow copy ModelAccount to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
        }