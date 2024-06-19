from abc import ABC, abstractmethod
import logging
from typing import Any, List


class ObjectDataBase(ABC):
    
    def __init__(self,db_session, log:logging.Logger):
        self.log = log
        self.log.info("ObjectDataBase class called")
        self.db_session = db_session

    @abstractmethod
    def create(self, auto_commit:bool=True) -> Any:
        
        """Create object model."""
        
    @abstractmethod
    def delete_all(self, auto_commit:bool= True) -> None:
        """Delete all Objects."""
        
    @abstractmethod
    def get(self, id:int) -> Any:
        """Get object model."""
    
    @abstractmethod   
    def get_all(self) -> List[Any]:
        """Get all objects."""
        pass     
    
    @abstractmethod
    def delete(self, id:int, auto_commit:bool= True):
        """delete a object"""
        pass
            
    def save_session_database(self)-> None:
        try:
            self.db_session.commit()
            self.log.info("save_session_database done !")
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: abstract_object method: save_session_database fail {e}")
            raise e
        