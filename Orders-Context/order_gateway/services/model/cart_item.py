from dataclasses import dataclass, fields


@dataclass
class CartItem:
    product_name: str
    brand: str
    description: str
    image: str
    size: str
    quantity: int
    price: float
    
    def __to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def to_dict(self):
        camel_case_dict = {}
        for field in fields(self):
            camel_case_key = self.__to_camel_case(field.name)
            camel_case_dict[camel_case_key] = getattr(self, field.name)
        return camel_case_dict