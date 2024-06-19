from dataclasses import dataclass, fields
from typing import List, Optional
from services.model.customer import Customer
from services.model.delivery import Delivery
from services.model.cart_item import CartItem


@dataclass
class CartOrder:
    order_id: str
    created_date: str
    created_time: str
    total: float
    customer_details: Customer
    delivery_details: Delivery
    order_details: List[CartItem]
    notes: Optional[str] = None

    def __to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def to_dict(self):
        camel_case_dict = {}
        
        for field in fields(self):
            camel_case_key = self.__to_camel_case(field.name)
            value = getattr(self, field.name)
            if isinstance(value, (list, tuple)):
                camel_case_dict[camel_case_key] = [v.to_dict() if isinstance(v, (CartOrder, Customer, Delivery, CartItem)) else v for v in value]
            elif isinstance(value, (CartOrder, Customer, Delivery, CartItem)):
                camel_case_dict[camel_case_key] = value.to_dict()
            else:
                camel_case_dict[camel_case_key] = value
        return camel_case_dict
