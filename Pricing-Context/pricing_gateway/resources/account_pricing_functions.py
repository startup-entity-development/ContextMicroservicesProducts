from pricing_ctx_database_sqlalchemy_14.models.model_pricing_account import ModelPricingAccount
from pricing_ctx_database_sqlalchemy_14.models.base import db_session
from pricing_ctx_database_sqlalchemy_14.models.model_pricing_profile import ModelPricingProfile
from pricing_ctx_database_sqlalchemy_14.objects.pricing_account_object import AccountPricingDataBase
from pricing_ctx_database_sqlalchemy_14.objects.pricing_profile_object import ProfilePricingDataBase
import logging

class AccountPricingFunctions():

    def __init__(self, external_account_id, **kwargs):
        self.external_account_id = external_account_id
        self.db_session = db_session
        self.log = logging.getLogger(__name__)
        self.pricing_profile_database = ProfilePricingDataBase(self.db_session, self.log)
        self.pricing_account_database = AccountPricingDataBase(self.db_session, self.log)
        super().__init__(**kwargs)

    def get_pricing_profile(self, role_name:str, level_name:str)->ModelPricingProfile:
        """Get the pricing profile by rule_name and level_name if not found return the default profile."""
        try:
            list_profile: ModelPricingProfile = self.pricing_profile_database.get_by_rule_level_name(rule_access_name= role_name, level_access_name= level_name)
            if isinstance(list_profile, list) and len(list_profile) > 0:
                return list_profile[0]
            else :
                return self.pricing_profile_database.create_default(rule_access_name= role_name, level_access_name= level_name)
        except Exception as e:
            self.log.error(f"file: get_account_pricing_cart.py method: get_pricing_profile fail {e}")
            raise e

    def get_account_pricing(self)->ModelPricingAccount|None:
        try:
            account_pricing = self.pricing_account_database.get_by_external_account_id(self.external_account_id)
            if isinstance(account_pricing, ModelPricingAccount):
                return account_pricing
            else:
                return None
        except Exception as e:
            self.log.error(f"file: get_account_pricing_cart.py method: get_account_pricing fail {e}")
            raise e

    def obtain_pricing_profile(self, rule_name:str, level_name:str)->ModelPricingProfile:
        try:
            account_profile:ModelPricingAccount = self.get_account_pricing()
            if account_profile:
                profile = account_profile.pricing_profile[0]
                if isinstance(profile, ModelPricingProfile):
                    return profile
            return self.get_pricing_profile(rule_name, level_name)
        except Exception as e:
            self.log.error(f"file: get_account_pricing_cart.py method: obtain_pricing_profile fail {e}")
            raise e
    
    def assign_pricing_profile(self, profile:ModelPricingProfile)-> ModelPricingAccount:
        try:
            account_pricing = self.get_account_pricing()
            if account_pricing:
                account_pricing = self.pricing_account_database.update_profile(id=account_pricing.id, pricing_profile_id=profile)
            else:
                account_pricing = self.pricing_account_database.create(external_account_id=self.external_account_id, pricing_profile_id=profile.id)
        except Exception as e:
            self.log.error(f"file: get_account_pricing_cart.py method: assign_pricing_profile fail {e}")
            raise e
        return account_pricing