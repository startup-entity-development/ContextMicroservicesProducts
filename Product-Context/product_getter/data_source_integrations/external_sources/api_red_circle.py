
import logging
from typing import Any, Dict, List

import urllib
from data_source_integrations.asynchronous_request import ShipperRequest
from data_source_integrations.external_sources.api_object import ApiSources

class RedCircle(ApiSources, ShipperRequest):
    def __init__(self, api_key:str="601DFD38194147719CB91034918E65F6",
                    endpoint:str="https://api.redcircleapi.com"):
        
        self.log = logging.getLogger(__name__)
        self.log.info(f"RedCircle class called")
        self.endpoint_base = endpoint
        self.api_key = api_key
        super().__init__(api_key,self.log ,endpoint)
        
    def get_main_categories(self) -> List[Dict[str,Any]]:
        params = {
        'api_key': self.api_key
        }
        return self.get_dic_response(params=params, route="/categories")["categories"] 
    
    def get_main_category_id(self,name_main_category:str ,list_dict_main_categories:List[Dict[str,Any]]) -> str|None:
        dict_main_category:Dict[str,Any] = {}
        for dict_main_category in list_dict_main_categories:
            if dict_main_category["name"] == name_main_category:
                return dict_main_category["id"]

        return None
    
    def get_categories(self, main_category_id:str) -> Dict:
        
        params = {
        'api_key': self.api_key,
            'parent_id': main_category_id
        }   
        return self.get_dic_response(params=params, route="/categories")["categories"]
    
    def get_sub_categories(self, api_category_id:str) -> Dict:
        self.get_categories(main_category_id=api_category_id)    


    def get_products_term(self, category_api_id:str, term_search:str) -> Dict|None:
        
        def request_search(term_request:str) -> Dict|None:
            products:Dict = {}
            
            term = urllib.parse.quote(term_request)
            params = {
            'api_key': self.api_key,
            'search_term':term ,
            'category_id': category_api_id,
            'type': 'search',
            'max_page': '5',
            }
            
            result = self.get_dic_response(params=params, route="/request")
            pagination = result.get("pagination", None)
            products["products"] = result.get("search_results", None)
            products["pagination"] = pagination
            return products
        
        
        search_results = request_search(term_request=term_search)
        
        if search_results:
            return search_results
        
        
        for i in range(0, 3):
            if i == 0:
                term = "highlighter pens"
                search_results = request_search(term_request=term)
            if i == 1:
                term = term_search.split(" ")[0]
                search_results = request_search(term_request=term)
            if i == 2:
                term = term_search.split(" ")[-1]
                search_results = request_search(term_request=term)
                    
            if search_results:
                break
        
        return search_results

    def get_products_by_category(self, subcategory_api_id:str) -> Dict|None:
        products:Dict = {}
        
        params = {
            'api_key': self.api_key,
            'type': 'category',
            'category_id': subcategory_api_id,
            'max_page': '5',}
        
        result = self.get_dic_response(params=params, route="/request")
        pagination = result.get("pagination", None)
        products["products"] = result.get("category_results", None)
        products["pagination"] = pagination
        return products
    
    
        
if __name__ == "__main__":
    # set up the request parameters
    red_circle = RedCircle()
    main_categories = red_circle.get_main_categories()
    id_grocery = red_circle.get_main_category_id(name_main_category="Grocery",
                                                 list_dict_main_categories=main_categories)
    assert id_grocery != None
    