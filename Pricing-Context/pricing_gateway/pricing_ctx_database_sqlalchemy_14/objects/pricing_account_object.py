import time
from pricing_ctx_database_sqlalchemy_14.models.model_pricing_account import ModelPricingAccount
from pricing_ctx_database_sqlalchemy_14.models.model_pricing_profile import ModelPricingProfile
from pricing_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase

class AccountPricingDataBase(ObjectDataBase):
    
    def __init__(self, db_session, log):
        self.log = log
        self.db_session = db_session
        super().__init__(db_session, log)

    def create(self, external_account_id:str, pricing_profile_id:int, auto_commit:bool=True) -> ModelPricingAccount:
        now = int(time.time())
        created = now
        
        try:
            account_pricing = ModelPricingAccount(external_account_id=external_account_id,
                                        pricing_profile_id=pricing_profile_id,
                                        created=created)

            self.db_session.add(account_pricing)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.db_session.refresh(account_pricing)
            return account_pricing
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: account_pricing_object.py method: create fail {e}")
            raise e
    
    def get(self, id:int) -> ModelPricingAccount:
        try:
            account_pricing = self.db_session.query(ModelPricingAccount).get(id)
            return account_pricing
        except Exception as e:
            self.log.error(f"file: account_pricing_object.py method: get fail {e}")
            raise e
    
    def get_all(self) -> list[ModelPricingAccount]:
        try:
            account_pricing = self.db_session.query(ModelPricingAccount).all()
            return account_pricing
        except Exception as e:
            self.log.error(f"file: account_pricing_object.py method: get_all fail {e}")
            raise e
    
    def delete(self, id:int, auto_commit:bool= True) -> None:
        try:
            account_pricing = self.get(id)
            self.db_session.delete(account_pricing)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: account_pricing_object.py method: delete fail {e}")
            raise e
    
    def delete_all(self, auto_commit:bool= True) -> None:
        try:
            self.db_session.query(ModelPricingAccount).delete()
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: account_pricing_object.py method: delete_all fail {e}")
            raise e
        
    def get_by_external_account_id(self, external_account_id:str) -> ModelPricingAccount:
        try:
            account_pricing = self.db_session.query(ModelPricingAccount).filter_by(external_account_id=external_account_id).first()
            return account_pricing
        except Exception as e:
            self.log.error(f"file: account_pricing_object.py method: get_by_external_account_id fail {e}")
            raise e
    
    def update_profile(self, id:int, pricing_profile:ModelPricingProfile, auto_commit:bool=True) -> ModelPricingAccount:
        try:
            account_pricing:ModelPricingAccount = self.db_session.query(ModelPricingAccount).get(id)
            account_pricing.pricing_profile = pricing_profile
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.db_session.refresh(account_pricing)
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: account_pricing_object.py method: update_profile fail {e}")
            raise e
        return account_pricing
            
        
