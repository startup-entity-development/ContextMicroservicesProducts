import time
from typing import List
from pricing_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase
from pricing_ctx_database_sqlalchemy_14.models.model_account_promotion import ModelAccountPromotion

class AccountPromotionDataBase(ObjectDataBase):
    
    def __init__(self, db_session, log):
        self.log = log
        self.db_session = db_session
        super().__init__(db_session, log)

    def create(self, id_account_pricing:int, id_promotion:int, auto_commit:bool=True) -> ModelAccountPromotion:
        now = int(time.time())
        created = now
        try:
            assert id_account_pricing, "id_account_pricing is required"
            assert id_promotion, "id_promotion is required"
            account_promotion = ModelAccountPromotion(id_account_pricing=id_account_pricing,
                                                        id_promotion=id_promotion,
                                                        created=created,
                                                        )

            self.db_session.add(account_promotion)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.db_session.refresh(account_promotion)
            return account_promotion
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: account_promotion_object.py method: create fail {e}")
            raise e

    def get(self, id:int) -> ModelAccountPromotion:
        assert isinstance(id, int), "id is required and must be an integer"
        try:
            account_promotion = self.db_session.query(ModelAccountPromotion).filter_by(id=id).first()
            return account_promotion
        except Exception as e:
            self.log.error(f"file: account_promotion_object.py method: get fail {e}")
            raise e

    def get_by_account_pricing_id(self, id_account_pricing:int) -> List[ModelAccountPromotion] | List:        
        try:
            assert isinstance(id_account_pricing, int), "id_account_pricing is required and must be an integer"
            account_promotion = self.db_session.query(ModelAccountPromotion).filter_by(id_account_pricing=id_account_pricing).all()
            if isinstance(account_promotion, list) and len(account_promotion) > 0:
                return account_promotion
            else:
                return []
        except Exception as e:
            self.log.error(f"file: account_promotion_object.py method: get_by_account_pricing_id fail {e}")
            raise e

    def get_by_id_promotion_id_account(self, id_promotion:int, id_account_pricing:int) -> ModelAccountPromotion:
        try:
            assert isinstance(id_promotion, int), "id_promotion is required and must be an integer"
            assert isinstance(id_account_pricing, int), "id_account_pricing is required and must be an integer"
            account_promotion = self.db_session.query(ModelAccountPromotion).filter_by(id_promotion=id_promotion, id_account_pricing=id_account_pricing).first()
            return account_promotion
        except Exception as e:
            self.log.error(f"file: account_promotion_object.py method: get_by_id_promotion_id_account fail {e}")
            raise e
    def get_all(self) -> list[ModelAccountPromotion]:
        try:
            account_promotion = self.db_session.query(ModelAccountPromotion).all()
            return account_promotion
        except Exception as e:
            self.log.error(f"file: account_promotion_object.py method: get_all fail {e}")
            raise e
    
    def delete(self, id:int, auto_commit:bool= True) -> None:
        try:
            account_promotion = self.get(id)
            self.db_session.delete(account_promotion)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: account_promotion_object.py method: delete fail {e}")
            raise e
    
    def delete_all(self, auto_commit:bool= True) -> None:
        try:
            self.db_session.query(ModelAccountPromotion).delete()
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: account_promotion   object.py method: delete_all fail {e}")
