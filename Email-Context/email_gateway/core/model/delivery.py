from dataclasses import dataclass


@dataclass
class Delivery:
    address: str
    delivery_date: str
    time_range: str
