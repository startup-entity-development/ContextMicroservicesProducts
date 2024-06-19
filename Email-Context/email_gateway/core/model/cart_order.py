from dataclasses import dataclass
from typing import List, Optional
from core.model.customer import Customer
from core.model.delivery import Delivery
from core.model.cart_item import CartItem


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

    def __post_init__(self):
        self.customer_details = Customer(**self.customer_details)
        self.delivery_details = Delivery(**self.delivery_details)
        self.order_details = [CartItem(**item) for item in self.order_details]
