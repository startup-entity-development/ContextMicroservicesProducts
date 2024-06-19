from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, List
import requests


class ApiSources (ABC):
    
    def __init__(self, api_key, log:logging.Logger, endpoint:str):
        self.api_key = api_key  
        self.endpoint_base = endpoint
        self.log = logging.getLogger(__name__)
        self.log.info(f"API class called")
    
    def get_dic_response(self, params:Dict, route:str ="") -> Dict  : 
        try:
            response = requests.get(f"{self.endpoint_base}{route}", params=params)
            response.raise_for_status()
        except Exception as ex:
            return {}
        return response.json()
    

    @abstractmethod
    def  get_categories(self, main_category_id:str) -> Dict:
        """Get categories from API ,return Dict of categories"""
        pass
    
    @abstractmethod
    def get_sub_categories(self) -> Dict:
        """Get sub categories from API ,return Dict of sub categories"""
        pass
    
    
    @abstractmethod
    def get_products_term(self) -> Dict:
        """Get sub categories from API ,return Dict of sub categories"""
        pass
    