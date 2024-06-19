
import time
from typing import List

import graphene
from pricing_ctx_database_sqlalchemy_14.models.model_promotion import ModelPromotion
from pricing_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase

class TypePromotion(graphene.Enum):
    percent = "percent"
    amount = "amount"
    

class WhereApplies(graphene.Enum):
    product_subtotal = "product_subtotal"
    delivery_fee = "delivery_fee"
    service_fee = "service_fee"

class PromotionDataBase(ObjectDataBase):
    
    def __init__(self, db_session, log):
        self.log = log
        self.db_session = db_session
        super().__init__(db_session, log)
        
    def create(self,auto_commit :bool=True, **kwargs) -> None:
        try:
            promotion = self.model(**kwargs)
            self.db_session.add(promotion)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: promotion_object.py method: create fail {e}")
            raise e

    def get(self, id:int) -> ModelPromotion:
        try:
            promotion = self.db_session.query(ModelPromotion).get(id)
            return promotion
        except Exception as e:
            self.log.error(f"file: promotion_object.py method: get fail {e}")
            raise e

    def get_all(self) -> list[ModelPromotion]:
        try:
            promotion = self.db_session.query(ModelPromotion).all()
            return promotion
        except Exception as e:
            self.log.error(f"file: promotion_object.py method: get_all fail {e}")
            raise e
    
    def delete(self, id:int, auto_commit:bool= True) -> None:
        try:
            promotion = self.get(id)
            self.db_session.delete(promotion)
            if auto_commit:
                self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: promotion_object.py method: delete fail {e}")
            raise e
    
    def delete_all(self, auto_commit:bool= True) -> None:
        try:
            self.db_session.query(ModelPromotion).delete()
            if auto_commit:
                self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: promotion_object.py method: delete_all fail {e}")
            raise e
    
    def get_by_rule_level_name(self, rule_name:str, level_name:str, active:bool=True) -> List[ModelPromotion] | None:
        """_summary_

        Args:
            rule_name (str): also known as role_name
            level_name (str): 
            active (bool, optional): _description_. Defaults to True.

        Raises:
            e: _description_

        Returns:
            List[ModelPromotion]:  by end_timestamp >= current_time and is_active or None
        """
        current_time = int(time.time())
        try:
            promotions = self.db_session.query(ModelPromotion).filter_by(rule_access_name=rule_name,
                                                                        level_access_name=level_name,
                                                                        is_active=active
                                                                        ).filter(ModelPromotion.end_timestamp >= current_time).all()
            if isinstance(promotions, list) and len(promotions) > 0:
                return promotions
            return None
        except Exception as e:
            self.log.error(f"file: promotion_object.py method: get_by_rule_level_name fail {e}")
            raise e
        
    def get_by_coupon_code(self, coupon_code:str, active:bool=True) -> ModelPromotion | None:
        """_summary_

        Args:
            coupon_code (str): 
            active (bool, optional): _description_. Defaults to True.

        Raises:
            e: _description_

        Returns:
            ModelPromotion:  by coupon_code and is_active or None
        """
        current_time = int(time.time())
        try:
            promotion = self.db_session.query(ModelPromotion).filter_by(coupon_code=coupon_code,
                                                                        is_active=active
                                                                        ).filter(ModelPromotion.end_timestamp >= current_time).first()
            if isinstance(promotion, ModelPromotion):
                return promotion
            return None
        except Exception as e:
            self.log.error(f"file: promotion_object.py method: get_by_coupon_code fail {e}")
            raise e