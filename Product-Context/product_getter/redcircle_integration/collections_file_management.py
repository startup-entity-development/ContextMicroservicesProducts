from typing import List
from redcircle_integration.product import ProductMediaRetailerAttributes, ProductFileSubCategoryResult, ProductResult, ProductResultDetailed
import ijson
from redcircle_integration.media import ImageResult, VideoResult


class RedCircleCollections():
    """
    This class is responsible for managing the collections of RedCircle data
    """
    
    
    
    def get_product_from_json_file(self, file_name:str="collection_product_details_redcircle/all_products_details_1.json") -> List[ProductResultDetailed]:    
        list_product_to_update: List[ProductResultDetailed]=[]
        product:ProductResultDetailed = None
        print(f"file_name:{file_name}")
        with open(file_name,encoding='utf-8') as input_file:
        # load json iteratively
            parser = ijson.parse(input_file)
            for prefix, event, value in parser:
               
                if (prefix, event) == ('item.result.product', 'start_map'):
                    product = ProductResultDetailed(tcin=None, upc=None, description=None)
                                            
                if (prefix.endswith('product.tcin') and event == 'string'):
                    product.tcin = int(value)
                if (prefix.endswith('product.upc') and event == 'string'):
                    product.upc = value
                if (prefix.endswith('product.description') and event == 'string'):    
                    product.description = value
               
        
                if product is not None  and (prefix, event) == ('item.result.product', 'end_map') : 
                    list_product_to_update.append(product)
        
        return list_product_to_update
    
    
    