from abc import ABC, abstractmethod
import logging
import time
from typing import Any, Dict, List
import requests

class ApiSources (ABC):

    def __init__(self, api_key, log:logging.Logger, endpoint:str):
        self.api_key = api_key  
        self.endpoint_base = endpoint
        self.log = logging.getLogger(__name__)
        self.log.info(f"API class called")
        self.max_retries = 3

    def get_dic_response(self, params:Dict, headers:Dict, route:str ="") -> Dict  : 
        counter = 0
        try:
           return self.request_data(params, headers, route)
        except Exception as ex:
            logging.error(f"Error in get_dic_response {ex}")
            if counter <= self.max_retries:
                counter += 1
                time.sleep(10)
                return self.request_data(params, headers, route)
            else:
                logging.error(f"Error in get_dic_response {ex} max retries reached")
                raise ex
         
    
    def request_data(self, params:Dict, headers:Dict, route:str ="") -> Dict:
        try:
            response = requests.get(f"{self.endpoint_base}{route}", params=params, headers=headers)
        except Exception as e:
            logging.error(f"Error in request_data {e}")
            raise e
        return response.json()

    @abstractmethod
    def get_all_categories(self, main_category_id:str) -> Dict:
        """Get categories from API ,return Dict of categories"""
        pass

    # @abstractmethod
    # def get_sub_categories(self) -> Dict:
    #     """Get sub categories from API ,return Dict of sub categories"""
    #     pass
    
