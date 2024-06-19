import copy
from typing import Any, Dict, List, Tuple
from dataclasses import dataclass
import json
from product_ctx_database_sqlalchemy_14.objects.utils import UnitMeasure


@dataclass
class MealmeArguments: 
    store_id: str
    pickup: bool
    include_quote: bool
    user_latitude:float
    user_longitude:float
    user_street_num:str
    user_street_name:str
    user_city:str
    user_state:str
    user_zipcode:str
    user_country:str

    @classmethod
    def from_dict(self, data: dict):
        for field in self.__dataclass_fields__.keys():
            setattr(self, field, data.get(field, None))
        return self
    
    @classmethod
    def to_dict(self) -> Dict[str, Any]:

        obj_dict = self.__dict__.copy()
        return {
            "store_id": obj_dict["store_id"],
            "pickup": obj_dict["pickup"],
            "include_quote": obj_dict["include_quote"],
            "user_latitude": obj_dict["user_latitude"],
            "user_longitude": obj_dict["user_longitude"],
            "user_street_num": obj_dict["user_street_num"],
            "user_street_name": obj_dict["user_street_name"],
            "user_city": obj_dict["user_city"],
            "user_state": obj_dict["user_state"],
            "user_zipcode": obj_dict["user_zipcode"],
            "user_country": obj_dict["user_country"],
        }
    
    def to_json(self) -> Dict[str, Any]:
        return json.dumps(self.to_dict()) 

@dataclass
class Product:
    name: str
    prince:int
    formatted_price:str
    is_available:bool
    unit_size:float
    unit_of_measurement:str
    description: str
    image:str
    product_id:str
    id_db:int = None
    id_media_db:int = None
    id_retailer_db:int = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "prince": self.prince,
            "formatted_price": self.formatted_price,
            "is_available": self.is_available,
            "unit_size": self.unit_size,
            "unit_of_measurement": self.unit_of_measurement,
            "description": self.description,
            "image": self.image,
            "product_id": self.product_id
        }
    
    def to_json(self) -> Dict[str, Any]:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(self, data: dict):
       return self(**data)
    
    def get_product_dimensions(self) -> Tuple[str,float,float]:
        """
        unit_m:str|None, size:float|None, weight:float|None
        """
        unit_m = UnitMeasure.get_unit_measure(self.unit_of_measurement)
        size = None
        weight = None
        if not unit_m or unit_m == "gallon":
            size = str(self.unit_size)
        else :
            weight = self.unit_size
        return unit_m, size, weight
    
    def get_dimensions_string(self) -> str:
        unit_m, size, weight = self.get_product_dimensions()
        return f"{unit_m} {size} {weight}"
    

@dataclass
class Subcategory:
    name: str
    subcategory_id: str
    products: List[Product]
    id_db:int = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "subcategory_id": self.subcategory_id,
            "products": [product.to_dict() for product in self.products]
        }

    @classmethod
    def from_dict(self, data: dict):
        list_dict = data.get("products", [])
        list_products:List[Product] = [Product.from_dict(product) for product in list_dict ]
        return self(name=data.get("name", None),
                    subcategory_id=data.get("subcategory_id", None),
                    products=list_products)
        
    
    def to_json(self) -> Dict[str, Any]:
        return json.dumps(self.to_dict())

@dataclass
class Category:
    name: str
    category_id: str
    subcategories: List[Subcategory] 
    id_db:int = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "category_id": self.category_id,
            "subcategories": [subcategory.to_dict() for subcategory in self.subcategories]
        }

    @classmethod
    def from_dict(self, data: dict):
        return self(name=data.get("name", None),
                    category_id=data.get("category_id", None),
                    subcategories=[Subcategory.from_dict(subcategory) for subcategory in data.get("subcategories", [])])

    def to_json(self) -> Dict[str, Any]:
        return json.dumps(self.to_dict())
    

@dataclass
class Collector:
    categories: List[Category]
    mealme_arguments: MealmeArguments
    id_retailer_db: int = None

    def to_json(self) -> Dict[str, Any]:
        return json.dumps({
            "categories": [category.to_dict() for category in self.categories],
            "mealme_arguments": self.mealme_arguments.to_dict(),
            "id_retailer_db": self.id_retailer_db
        })
    
    def to_file(self, path:str) -> None:
        with open(path, "w") as file:
            file.write(self.to_json())
    
    @classmethod
    def from_json(self, data_json: str):
        for field in self.__dataclass_fields__.keys():
            dict_data = json.loads(data_json)
            if field == "categories":
                setattr(self, field, [Category.from_dict(category) for category in dict_data.get(field, [])])
            elif field == "mealme_arguments":
                setattr(self, field, MealmeArguments.from_dict(dict_data.get(field, {})))
            else:
                setattr(self, field, dict_data.get(field, None))
        return self
    
    @classmethod
    def from_file(self, path:str):
        with open(path, "r") as file:
            data = file.read()
        return self.from_json(data)