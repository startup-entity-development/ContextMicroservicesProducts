from dataclasses import dataclass, fields


@dataclass
class Customer:
    email: str
    name: str
    phone: str
    
    def __to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def to_dict(self):
        camel_case_dict = {}
        for field in fields(self):
            camel_case_key = self.__to_camel_case(field.name)
            camel_case_dict[camel_case_key] = getattr(self, field.name)
        return camel_case_dict
