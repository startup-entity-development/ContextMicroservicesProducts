

from functools import lru_cache
from pricing_ctx_database_sqlalchemy_14.objects.weight_delivery_object import WeightDeliveryDataBase


class DeliveryFeeBasedInWight(WeightDeliveryDataBase):

    def __init__(self, **kwargs):
        self.log = kwargs.get('log')
        self.db_session = kwargs.get('db_session')
        super().__init__(**kwargs)

    @lru_cache
    def get_price_weight_delivery(self, weight:float):
        return self.get_by_weight(weight)

    def clear_cache(self):
        self.get_table_weight_delivery.cache_clear()

    def get_delivery_fee(self, delivery_fee_base:float, weight:float):
        weight_delivery = self.get_price_weight_delivery(weight)
        if weight_delivery:
            return weight_delivery.price_delivery + delivery_fee_base

        return delivery_fee_base