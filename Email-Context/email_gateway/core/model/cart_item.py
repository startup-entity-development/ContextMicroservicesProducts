from dataclasses import dataclass


@dataclass
class CartItem:
    product_name: str
    brand: str
    description: str
    image: str
    size: str
    quantity: int
    price: float
