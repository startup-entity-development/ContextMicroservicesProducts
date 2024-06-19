

import dataclasses
from typing import Any, Dict, List
import requests



@dataclasses.dataclass
class ProductBarcodeLookupAttributes:
    
    def __init__(self) -> None:
        self.barcode_number:str
        self.title:str
        self.brand:str
        self.description:str
        self.nutrition_facts:str
        self.category:str
        self.size:str
        self.images:List[str]
        
    def __str__(self) -> str:
        
        return f"""
        barcode_number: {self.barcode_number}
        title: {self.title}
        brand: {self.brand}
        description: {self.description}
        nutrition_facts: {self.nutrition_facts}
        category: {self.category}
        size: {self.size}
        images: {self.images}
        """
    def to_dict(self) -> Dict[str, Any]:
        """return  shallow copy of object as dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            }
    
class ProductBarcodeLookup:
    
    def __init__(self):
        self.api_key = "7mahmu1dn8r3cuqzxzwj11aj7c1e8p"
        self.url = "https://api.barcodelookup.com/v3/products"

    def _get_product_by_upc_code(self, upc_code) -> dict|None:
        
        params = {
            "barcode": upc_code,
            "formatted": "true",
            "key": self.api_key
        }
        try:
            response = requests.get(self.url, params=params)
            if response.status_code != 200:
                return None
        except :
            return None
        return response.json()
    
    def _response_to_product_attributes(self, result_product):
        try:
            result_product = result_product.get('products')[0]
            product_attributes = ProductBarcodeLookupAttributes()
            product_attributes.barcode_number = result_product.get('barcode_number')
            product_attributes.title = result_product.get('title')
            product_attributes.brand = result_product.get('brand')
            product_attributes.description = result_product.get('description')
            product_attributes.nutrition_facts = result_product.get('nutrition_facts')
            product_attributes.category = result_product.get('category')
            product_attributes.size = result_product.get('size')
            product_attributes.images = result_product.get('images') 
        except:
            return None
        return product_attributes
    
    
    def get_product_attributes(self, upc_code:str):
        
        if upc_code == None:
            raise ValueError("upc_code is required")
        if type(upc_code) != str:
            raise TypeError("upc_code must be a string")
       
        
        result_product = self._get_product_by_upc_code(upc_code)
        if result_product == None:
            raise Exception(f"Failed to get product from api call to barcodelookup.com, upc_code: {upc_code}")
        product_attributes = self._response_to_product_attributes(result_product)
        if product_attributes == None:
            raise Exception(f"Failed to parse product attributes from api call to barcodelookup.com, upc_code: {upc_code} ")
        return product_attributes

if __name__ == "__main__":
    product_barcode_lookup = ProductBarcodeLookup()
    product_attributes = product_barcode_lookup.get_product_attributes("041500000428")
    print(product_attributes)

    