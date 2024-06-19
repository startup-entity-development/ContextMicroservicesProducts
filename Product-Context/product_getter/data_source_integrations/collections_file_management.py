from typing import List
from data_source_integrations.product import ProductAttributesMedia, ProductFileSubCategoryResult, ProductResult, ProductResultDetailled
import ijson
from data_source_integrations.media import ImageResult, VideoResult


class RedCircleCollections():
    """
    This class is responsible for managing the collections of RedCircle data
    """
    
    
    
    def get_product_from_json_file(self, file_name:str="collection_product_details_redcircle/all_products_details_1.json") -> List[ProductResultDetailled]:    
        list_product_to_update: List[ProductResultDetailled]=[]
        product:ProductResultDetailled = None
        print(f"file_name:{file_name}")
        with open(file_name,encoding='utf-8') as input_file:
        # load json iteratively
            parser = ijson.parse(input_file)
            for prefix, event, value in parser:
               
                if (prefix, event) == ('item.result.product', 'start_map'):
                    product = ProductResultDetailled(tcin=None, upc=None, description=None)
                                            
                if (prefix.endswith('product.tcin') and event == 'string'):
                    product.tcin = int(value)
                if (prefix.endswith('product.upc') and event == 'string'):
                    product.upc = value
                if (prefix.endswith('product.description') and event == 'string'):    
                    product.description = value
               
        
                if product is not None  and (prefix, event) == ('item.result.product', 'end_map') : 
                    list_product_to_update.append(product)
        
        return list_product_to_update
    
    
    