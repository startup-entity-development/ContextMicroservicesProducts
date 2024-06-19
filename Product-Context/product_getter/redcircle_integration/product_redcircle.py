from json import loads
from product_ctx_database_sqlalchemy_14.models.product_model import ModelProduct
import ijson
import logging
from typing import Any, Dict, List
from product_ctx_database_sqlalchemy_14.models.category_model import ModelCategory
from product_ctx_database_sqlalchemy_14.objects.media_object import MediaAttributes
from product_ctx_database_sqlalchemy_14.objects.product_object import ProductAttributes
from product_ctx_database_sqlalchemy_14.objects.product_retailer import ProductRetailerAttributes
from product_ctx_database_sqlalchemy_14.objects.utils import UnitMeasure
from redcircle_integration.collections_file_management import RedCircleCollections
from redcircle_integration.category_redcircle import CategoryRedCircle
from redcircle_integration.external_sources.api_red_circle import RedCircle
from redcircle_integration.media import ImageResult, MediaRedCircle, VideoResult
from redcircle_integration.pagination.pagination import Pagination, PaginationFunctionClass
from redcircle_integration.product import Product, ProductMediaRetailerAttributes, ProductFileSubCategoryResult, ProductResult, ProductResultDetailed, ProductSearchResult, ResultGetFromAPI
from redcircle_integration.sub_category_redcircle import SubCategoryRedCircle


class ProductRedCircle(Product, PaginationFunctionClass,RedCircleCollections):

    def __init__(self, category_red_circle:CategoryRedCircle,
                    subcategory_red_circle:CategoryRedCircle ) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info(f"ProductRedCircle class called")
        self.api_object:RedCircle= RedCircle()
        self.media_red_circle:MediaRedCircle = MediaRedCircle()
        self.category_red_circle:CategoryRedCircle = category_red_circle
        self.subcategory_red_circle:SubCategoryRedCircle = subcategory_red_circle
        super().__init__(api_object=self.api_object)
        self.subcategories_success_products:List[ResultGetFromAPI] = []
        self.load_list_success_sub_category_product_from_file_json()

    def load_list_success_sub_category_product_from_file_json(self, file_name:str="success_subcategories.json") -> None:
        with open(file_name, "r") as file:
            file_list_subcategories_product_success:List[Dict[str, Any]] = file.read()
            if not file_list_subcategories_product_success:
                return
            file_list_subcategories_product_success = loads(file_list_subcategories_product_success)
            for subcategory_success_products in file_list_subcategories_product_success:
                self.subcategories_success_products.append(ResultGetFromAPI(id_database=subcategory_success_products["id_database"],
                                                                                            id_api=subcategory_success_products["id_api"],
                                                                                            term=subcategory_success_products["term"]))    
            self.log.info(f"load_list_success_sub_category_product_from_file_json: {self.subcategories_success_products}")

    def create_success_sub_category_product_from_file_json(self, file_name:str="success_subcategories.json") -> None:
        with open(file_name, "w") as file:
            file.truncate(0)
            file.write("[")
            for subcategory_success_products in self.subcategories_success_products:
                file.write(subcategory_success_products.json_string)
                if subcategory_success_products != self.subcategories_success_products[-1]:
                    file.write(",")
            file.write("]")

    def _pull_products_raw(self, api_id_category:str, api_id_subcategory:str, term:str, search:bool=False) -> List[Dict[str, Any]] | None | str:
        list_id_api_sub_cat_success:str = [subcategory.id_api for subcategory in self.subcategories_success_products]
        
        if api_id_subcategory in list_id_api_sub_cat_success:
            self.log.info(f"api_id_subcategory: {api_id_subcategory} already in list_id_api_sub_cat_success") 
            return "currently_in_db"
        if search:
            dict_result:Dict[str, Any] = self.api_object.get_products_term(category_api_id=api_id_category,
                                                                         term_search=term)
        else:
            dict_result:Dict[str, Any] = self.api_object.get_products_by_category(subcategory_api_id=api_id_subcategory)
        
        if not isinstance(dict_result, dict):
            return None
        if not dict_result:
            return None    
        return dict_result
    
    def get_products_results(self, api_id_category:str, api_id_subcategory:str , term:str) -> List[ProductSearchResult] | None | str: 
        
        dict_result:Dict[str, Any] = self._pull_products_raw(api_id_category=api_id_category,
                                                                api_id_subcategory=api_id_subcategory,
                                                                term=term)  
        if dict_result == "currently_in_db":
            return "currently_in_db"
       
        list_result_product:List[Dict[str, Any]] = dict_result.get("products", None)
        pagination_dict:Dict[str, Any] = dict_result.get("pagination", None)

        
        if list_result_product is None:
            return None
        
        list_product_search_result:List[ProductSearchResult] = []

        for result_product in list_result_product:
        
            title:str = result_product["product"].get("title", "")
            brand:str = result_product["product"].get("brand", "")
            link:str = result_product["product"].get("link", "")
            price:float = result_product["offers"]["primary"].get("price", 0) 
            dpci:str = result_product["product"].get("dpci")
            tcin:int = int(result_product["product"].get("tcin"))
            images:List[Dict[str,Any]] = result_product["product"].get("images", [])
            main_image:str = result_product["product"].get("main_image", None)
            videos:List[Dict[str,Any]] = result_product["product"].get("videos", [])
            product_features_bullets:List[str] = result_product["product"].get("feature_bullets", [""])
            

            if images:
                product_images_result:List[ImageResult] = [ImageResult(link=image) for image in images ]
            else:
                product_images_result:List[ImageResult] = []
            if main_image:
                product_images_result.append(ImageResult(link=main_image, is_main=True))
            if videos:
                product_videos_result:List[VideoResult] = [VideoResult(link=video["link"], type=video["type"] ) for video in videos ]
            else:
                product_videos_result:List[VideoResult] = []   
                           
            product_result:ProductResult = ProductResult(title=title,
                                                         link=link,
                                                         dpci=dpci,
                                                         tcin=tcin,
                                                         price=price,
                                                         brand=brand,
                                                         feature_bullets=product_features_bullets,
                                                         images=product_images_result,
                                                         videos=product_videos_result)

            # pagination:Pagination = Pagination(next_link=pagination_dict.get("next", None),
            #                                     prev_link=pagination_dict.get("prev", None),
            #                                     total_pages=pagination_dict.get("total_pages", None),
            #                                     current_page=pagination_dict.get("current_page", None),
            #                                     total_results=pagination_dict.get("total_results", None))
            
            
            product_search_result:ProductSearchResult = ProductSearchResult(pagination=None,
                                                                            products=product_result)
            list_product_search_result.append(product_search_result)

        return list_product_search_result
        
    
    def _pull_products_by_categories(self, start:int, to:int) -> List[ProductMediaRetailerAttributes]:
        
        list_categories:List[ModelCategory] = self.category_red_circle.object_database.get_all()[start:to]
        list_products_search_result:List[ProductMediaRetailerAttributes] = []
        for category in list_categories:
            list_products_search_result.extend(self._pull_products_media_by_subcategories_db(category_db_id=category.id,
                                                                                                category_api_id=category.api_id))
            
            
        return list_products_search_result
    def remove_dirty_text_from_string(self, string:str,) -> str:
            list_dirty_text:List[str] = ["&#39;", "Gather&#8482;", "Good &#38;","&#38;","Day&#8482;" , "Cr&#232;",
                                         "&#8482;","&#233;", "&#8211", "<br /><br />", "<br /><br />",
                                         "<br />", "<br>", "&#174;", "&#8482;", "&#8480", "Good &"]
            for text in list_dirty_text:
               string = string.replace(text, "")
            return string
        
    def get_product_attributes_media(self, product_result:ProductResult, api_id:str, id_db_subcategory:int) -> ProductMediaRetailerAttributes:
        
            
        def get_name(text:str) -> str:
            if text.find(" - ") != -1:
                name:str = text.split(" - ")[0].strip()[:99]
            else:
                return text
            return name
        
        def get_description(product_result:ProductResult) -> str:
            description:str = ""
            
            if product_result.feature_bullets:
                for feature_bullet in product_result.feature_bullets:
                    if feature_bullet:
                        description = f"{description}{feature_bullet} \n"
                return description[:2500]
            
            return description
        
        def check_if_hast_numbers(string_input:str) -> bool:
            for character in string_input:
                if character.isdigit():
                    return True
            return False
        
        
        def get_measure_unit(title_fixed:str) -> UnitMeasure | None:
            
            title_fixed = title_fixed.lower()
        
            if title_fixed.find("- ") != -1:
                list_element_possible = title_fixed.split("- ")
                list_enum_unit = [unit.name for unit in UnitMeasure]
                if not list_element_possible:
                    return None
                # reverse list 
                list_element_possible = list_element_possible[::-1]
                for element in list_element_possible:
                    for unit in list_enum_unit:
                        # if element has a unit measure and numbers 
                        if element.find(unit) != -1 and check_if_hast_numbers(element) :
                            return UnitMeasure[unit]
            return None
        
        
        def get_unit_in_pack(title_fixed:str) -> int:
            
            if title_fixed.find("- ") != -1:
                list_element_possible = title_fixed.split("- ")
                list_element_possible = list_element_possible[::-1]
            else:
                list_element_possible = [title_fixed]
                
            for element_title in list_element_possible:  
                list_element_divisor = ["/", "-", " "]
                element_title = element_title.lower()
                element_indicate_unit = ["ct", "pk", "case of", "slices" ]
                for element_unit in element_indicate_unit:
                    unit_in_pack = None
                    if element_title.find(element_unit) != -1:
                        for divisor in list_element_divisor:
                            if element_title.find(divisor) != -1:
                                list_fragment :str = element_title.split(divisor)
                                for element in list_fragment:   
                                    if element.find(element_unit) != -1:    
                                        possible_measurement_data = element
                                        possible_measurement_data = possible_measurement_data.strip()
                                        unit_in_pack = take_int_first_number(possible_measurement_data)

                                        if unit_in_pack:
                                            return unit_in_pack
                if not unit_in_pack:
                    return 1
                            
                    
            return 1
        def take_float_first_number(string_input :str,) -> float | None:
            string_text:str = ""
            for character in string_input:
                if character.isdigit() or character == ".":
                    string_text = string_text + character
                if string_text != "" and (not character.isdigit() and character != "."):
                    break
            if string_text != "":
                try: 
                    return float(string_text)
                except:
                    return None 
            return None
    
       
        def take_int_first_number(string_input :str) -> int | None:
            string_text:str = ""
            
            for character in string_input:
                if character.isdigit():
                    string_text = string_text + character
                if string_text != "" and not character.isdigit():
                    break
            if string_text:
                return int(string_text)
            else:
                return None
            
        def get_weight(title_fixed:str, unit_measure:str) -> float | None:
            if title_fixed.find("- ") != -1:
                list_element_possible:List[str] = title_fixed.split("- ")
                list_element_possible = list_element_possible[::-1]
                
                weight:float = None
                for element in list_element_possible:
                    if not check_if_hast_numbers(element):
                        continue
                    possible_measurement_data = element.lower()
                    if possible_measurement_data.find("/")  != -1:
                
                        list_possible_measurement_data = possible_measurement_data.split("/")
                        
                        for possible_element in list_possible_measurement_data:
                            if possible_element.find(unit_measure.name) != -1 and check_if_hast_numbers(possible_element):
                                possible_measurement_data = possible_element
                                break                          
                     # extract float number from string, filter isdigit and "." and stop when find a " "
                    possible_measurement_data = possible_measurement_data.strip()
                    weight  = take_float_first_number(possible_measurement_data)
                    if weight:
                        return weight 
                
            return None
        
        
        title_fixed = self.remove_dirty_text_from_string(product_result.title)

        
        unit_measure:UnitMeasure = get_measure_unit(title_fixed)
        
        weight:float = None
        
        unit_in_pack:int = get_unit_in_pack(title_fixed)
        
        if unit_measure is not None:
            weight:str=get_weight(title_fixed, unit_measure)
            
        
        product_attributes:ProductAttributes = ProductAttributes(sub_category_id=id_db_subcategory,
                                                                api_id=f"api{api_id}_dpci:{product_result.dpci}_tcin:{product_result.tcin}",
                                                                name=get_name(title_fixed),
                                                                title=title_fixed,
                                                                brand=product_result.brand,
                                                                base_increment=13,
                                                                description=get_description(product_result=product_result),
                                                                upc_barcode=None,
                                                                unit_measure=unit_measure,
                                                                weight=weight,
                                                                unit_in_pack=unit_in_pack,
                                                                size=None,
                                                                cost=product_result.price,
                                                                dpci=product_result.dpci,
                                                                tcin=product_result.tcin
                                                                )
        product_retailer_attributes:ProductRetailerAttributes = ProductRetailerAttributes(retailer_id=1,
                                                                                            product_id=None,
                                                                                            link_url=product_result.link,
                                                                                            cost=product_result.price,
                                                                                            increment_retailer=1,
                                                                                            stock=1,
                                                                                            is_active=True,
                                                                                            is_in_stock=True
                                                                                            )    
                                                
        product_attributes_media:ProductMediaRetailerAttributes = ProductMediaRetailerAttributes(product_attributes=product_attributes,
                                                                                    product_retailer_attributes=product_retailer_attributes,
                                                                                    images=product_result.images,
                                                                                    videos=product_result.videos)
        
        
        return product_attributes_media
    
    def _pull_products_media_by_subcategories_db(self,category_db_id:int, category_api_id:str) -> List[ProductMediaRetailerAttributes]:
        list_products_media:List[ProductMediaRetailerAttributes] = []
        
        list_subcategories:List[ModelCategory] = self.subcategory_red_circle.object_database.get_by_category_id(category_id=category_db_id)
        
        
            
        for subcategory in list_subcategories:
            list_products_search_result:List[ProductSearchResult] = self.get_products_results(api_id_category=category_api_id,
                                                                                              api_id_subcategory=subcategory.api_id, 
                                                                                              term=subcategory.name)
            if list_products_search_result == "currently_in_db":
                continue
            
            if list_products_search_result is None:
                self.log.error(f"list_result is not a list subcategory_api_id: {subcategory.api_id} term: {subcategory.name} ")
                continue 
             # add subcategory to success list, posterior save in file
            self.subcategories_success_products.append(ResultGetFromAPI(id_database=subcategory.id,
                                                                        id_api=subcategory.api_id,
                                                                        term=subcategory.name))
            
            for product_search_result in list_products_search_result:
                product_attributes_media:ProductMediaRetailerAttributes = self.get_product_attributes_media(product_result=product_search_result.products,
                                                                                                    api_id=subcategory,
                                                                                                    id_db_subcategory=subcategory.id)                
                                                                            
                list_products_media.append(product_attributes_media)
                
        return list_products_media
    
    def update_database_from_request(self, start:int=0, to:int=1) -> None:
        list_product_attr_media:List[ProductMediaRetailerAttributes] = self._pull_products_by_categories(start=start, to=to)   
        self.update_database(list_product_attr_media=list_product_attr_media)
        
    def update_database(self, list_product_attr_media:List[ProductMediaRetailerAttributes]) -> None:
        for product_attr_media in list_product_attr_media:
            product_retailer_attributes:ProductRetailerAttributes = product_attr_media.product_retailer_attributes
            product_db = self.object_database.create(product=product_attr_media.product_attributes, auto_commit=True)
            if product_db is None:
                self.log.error(f"product_attr: {product_attr_media} fail to save in db")
                continue
            product_retailer_attributes.product_id = product_db.id
            self.product_retailer_db.create(product_retailer_attributes=product_attr_media.product_retailer_attributes,
                                            auto_commit=False)
            
            
            media_attrs_of_product:List[MediaAttributes]= self.media_red_circle.get_list_media_attr_from_images_videos(product_id=product_db.id,
                                                                                                                        images=product_attr_media.images,
                                                                                                                        videos=product_attr_media.videos)
            self.media_red_circle.update_database(list_media_of_product_attr=media_attrs_of_product)

        self.object_database.save_session_database()
         
                     
    def create_products_cvs_file_bunch_request(self):
        products_list:List[ModelProduct] = self.object_database.get_all()
        f = open("product_collection_redcircle.csv", "a")
        for product in products_list:
            f.write(f'\n "{product.tcin}","product",,,,,,,,,,,,,,,,,')
        f.close()
         
 
    def create_initial_pagination(self, list_product_search_result) -> None:
        for product_search_result in list_product_search_result:
            self.create_initial_pagination(product_search_result.pagination)
        
        self.save_list_of_initial_pagination()
        
        
    def get_next_link():
        pass
    
    def get_prev_link():
        pass
    
    def update_product_details_from_file_json(self, folder_name:str="collection_product_details_redcircle/",start_file:int=1 ,end_file:int=16) -> None:
        
        def create_list_source_file() -> List[str]:
            list_source_file:List[str] = []
            for i in range(start_file, end_file + 1):
                list_source_file.append(f"{folder_name}all_products_details_{i}.json")
            return list_source_file
        
        for file_name in create_list_source_file():
            list_product_details:List[ProductResultDetailed] = self.get_product_from_json_file(file_name=file_name)
            self.update_upc_and_description(list_product_details= list_product_details)
    
    def update_upc_and_description(self, list_product_details:List[ProductResultDetailed]) -> None:
        for product_detail in list_product_details:
            product_db:ModelProduct = self.object_database.get_by_tcin(tcin=product_detail.tcin)
            if product_db is None:
                self.log.error(f"product_db is None for product_detail: {product_detail}")
                continue
            product_db.upc_barcode = product_detail.upc
            if product_detail.description is not None:

                product_db.description = product_detail.description[:2500]
                product_db.description = self.remove_dirty_text_from_string(product_db.description) 
            self.object_database.save_session_database()
    
    
    def load_product_from_json_file(self, file_name:str="all_subcategories_products.json") -> None:    
        productFile:ProductFileSubCategoryResult=None
        product:ProductResult = None

        with open(file_name,encoding='utf-8') as input_file:
        # load json iteratively
            parser = ijson.parse(input_file,)
            for prefix, event, value in parser:
                if (prefix, event) == ('item.result.request_parameters.category_id', 'string'):
                    if product is not None and productFile is not None : 
                        list_product_attr_media:List[ProductMediaRetailerAttributes] = []
                        id_subcategory_db:int = self.subcategory_red_circle.object_database.get_by_id_api(id_api=productFile.id_subcategory_api).id
                        for product_result in productFile.products:
                            product_attr_media:ProductMediaRetailerAttributes = self.get_product_attributes_media(product_result=product_result,
                                                                                                          api_id=productFile.id_subcategory_api,
                                                                                                          id_db_subcategory=id_subcategory_db)
                            list_product_attr_media.append(product_attr_media)  
                                       
                        self.update_database(list_product_attr_media=list_product_attr_media)
                        
        
                    productFile = ProductFileSubCategoryResult(id_subcategory_api=value, products=[])
                    # products = ijson.items(input_file, 'result.category_results.item')
                    # for k,v in products:
                    #     print(k,v)
                if (prefix, event) == ('item.result.category_results.item.product', 'start_map'):
                    
                    product = ProductResult(title="",
                                            link="",
                                            dpci=None,
                                            tcin=None,
                                            price=0,
                                            brand="",
                                            feature_bullets=[],
                                            images=[],
                                            videos=[])
                    
                if (prefix.endswith('item.product.title') and event == 'string'):
                    product.title = value
                if (prefix.endswith('item.product.brand') and event == 'string'):
                    product.brand = value
                if (prefix.endswith('item.product.link') and event == 'string'):    
                    product.link = value
                if (prefix.endswith('item.product.dpci') and event == 'string'):
                    product.dpci = value
                if (prefix.endswith('item.product.tcin') and event == 'string'):
                    product.tcin = int(value)
                if (prefix.endswith('item.result.category_results.item.offers.primary.price') and event == 'number'):
                    product.price = value
                if (prefix.endswith('item.product.feature_bullets.item') and event == 'string'):
                    product.feature_bullets.append(value)
                if (prefix.endswith('item.product.main_image') and event == 'string'):
                    product.images.append(ImageResult(link=value, is_main=True))
                if (prefix.endswith('item.product.images.item') and event == 'string'):
                    product.images.append(ImageResult(link=value))
                if (prefix.endswith('item.product.videos.item.link') and event == 'string'):
                    product.videos.append(VideoResult(link=value, type="video/mp4"))
                                
        
                if product is not None and productFile is not None and (prefix, event) == ('item.result.category_results.item', 'end_map') and product.price != 0: 
                    productFile.products.append(product)
                