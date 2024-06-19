import logging
from typing import List
from pricing_ctx_database_sqlalchemy_14.models.model_account_promotion import ModelAccountPromotion
from pricing_ctx_database_sqlalchemy_14.models.base import db_session
from pricing_ctx_database_sqlalchemy_14.models.model_promotion import ModelPromotion
from pricing_ctx_database_sqlalchemy_14.objects.account_promotion_object import AccountPromotionDataBase
from pricing_ctx_database_sqlalchemy_14.objects.promotion_object import PromotionDataBase

class AccountPromotionFunctions():
    
    def __init__(self, account_pricing_id, **kwargs):
        self.account_pricing_id:int = account_pricing_id
        self.db_session = db_session
        self.log = logging.getLogger(__name__)
        self.account_promotion_db = AccountPromotionDataBase(self.db_session, self.log)
        self.promotion_db = PromotionDataBase(self.db_session, self.log)
        super().__init__(**kwargs)

    def update_promotions_accounts(self, rule_name:str, level_name:str) -> List[ModelPromotion]:
        list_of_current_promotions:List[ModelPromotion] = []
        try:
            list_model_account_promotion:List[ModelAccountPromotion] = self.account_promotion_db.get_by_account_pricing_id(id_account_pricing=self.account_pricing_id)
            if list_model_account_promotion:
                for promo_account_model in list_model_account_promotion:
                    promotion:ModelPromotion = promo_account_model.promotion
                    list_of_current_promotions.append(promotion)
        
            new_promotions = self.promotion_db.get_by_rule_level_name(rule_access_name=rule_name, level_access_name=level_name)
            if new_promotions:
                for promo in new_promotions:
                    if promo not in list_of_current_promotions:
                        new_promo_account = self.account_promotion_db.create(id_account_pricing=self.account_pricing_id, id_promotion=promo.id)
                        list_model_account_promotion.append(new_promo_account)
            return list_model_account_promotion
        except Exception as e:
            self.log.error(f"file: account_promotion_functions.py method: get_promotion fail {e}")
            raise e

    def add_promotion_by_coupon_code(self, coupon_code:str) -> ModelAccountPromotion|None:
        """Add a promotion to the account by coupon code
        If the promotion is not found return None
        if the promotion is found and the account_promotion not found create the account_promotion and return it
        if the promotion is already in account_promotion added return the account promotion
        """
        try:
            promotion = self.promotion_db.get_by_coupon_code(coupon_code=coupon_code)
            
            if promotion:
                account_promotion = self.account_promotion_db.get_by_id_promotion_id_account(id_promotion=promotion.id, id_account_pricing=self.account_pricing_id)
                if account_promotion:
                    return account_promotion
                
                new_promo_account = self.account_promotion_db.create(id_account_pricing=self.account_pricing_id, id_promotion=promotion.id)
                return new_promo_account
            else:
                return None
        except Exception as e:
            self.log.error(f"file: account_promotion_functions.py method: add_promotion_by_coupon_code fail {e}")
            raise e
        