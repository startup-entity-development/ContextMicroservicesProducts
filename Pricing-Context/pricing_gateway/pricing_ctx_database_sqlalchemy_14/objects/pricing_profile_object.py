
import time
from typing import List
from venv import create
from pricing_ctx_database_sqlalchemy_14.models.model_pricing_profile import ModelPricingProfile
from pricing_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase


class ProfilePricingDataBase(ObjectDataBase):
    def __init__(self, db_session, log):
        self.log = log
        self.db_session = db_session
        super().__init__(db_session, log)
        
    def create(self, auto_commit:bool=True, **kwargs) -> ModelPricingProfile:
        try:
            now = int(time.time())
            kwargs["created"] = now
            profile_pricing = ModelPricingProfile(**kwargs)
            self.db_session.add(profile_pricing)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.db_session.refresh(profile_pricing)
            return profile_pricing
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: profile_pricing_object.py method: create fail {e}")
            raise e
    
    def get(self, id: int) -> ModelPricingProfile:
        try:
            profile_pricing = self.db_session.query(ModelPricingProfile).get(id)
            return profile_pricing
        except Exception as e:
            self.log.error(f"file: profile_pricing_object.py method: get fail {e}")
            raise e
    
    def get_all(self) -> list[ModelPricingProfile]:
        """Get all profile pricing order by highest priority first"""
        try:
            #order by highest priority 
            profile_pricing = self.db_session.query(ModelPricingProfile).order_by(ModelPricingProfile.priority.desc()).all()
            return profile_pricing
        except Exception as e:
            self.log.error(f"file: profile_pricing_object.py method: get_all fail {e}")
            raise e
    
    def get_by_rule_level_name(self, rule_access_name:str, level_access_name:str) -> List[ModelPricingProfile]:
        """Get all profile pricing by rule_access_name and level_access_name order by highest priority first"""
        try:
            profile_pricing = self.db_session.query(ModelPricingProfile).filter_by(rule_access_name=rule_access_name,
                                                                                    level_access_name=level_access_name).order_by(ModelPricingProfile.priority.desc()).all()
            
            return profile_pricing
        except Exception as e:
            self.log.error(f"file: profile_pricing_object.py method: get_by_rule_level_name fail {e}")
            raise e
    
    def create_default(self, auto_commit:bool=True,** kwargs) -> ModelPricingProfile:
        name_profile = kwargs.get("name_profile", "default_pricing_profile")
        now = int(time.time())
        tax = kwargs.get("tax", 6)
        
        delivery_fee_base = kwargs.get("delivery_fee_base", 0)
        service_fee_base = kwargs.get("service_fee_base", 0)
        minimum_subtotal = kwargs.get("minimum_subtotal", 30)
        rule_access_name = kwargs.get("rule_access_name", None)
        level_access_name = kwargs.get("level_access_name", None)
        the_lower_profile_priority = self.get_lower_priority_profile()
        priority = kwargs.get("priority", self.get_next_lower_priority(priority_base=the_lower_profile_priority))
        description = kwargs.get("description", "The default profile rule access by setting")
        
        try:
            profile_pricing = ModelPricingProfile(name_profile=name_profile,
                                                    tax=tax,
                                                    delivery_fee_base=delivery_fee_base,
                                                    service_fee_base=service_fee_base,
                                                    minimum_subtotal=minimum_subtotal,
                                                    rule_access_name=rule_access_name,
                                                    level_access_name=level_access_name,
                                                    priority=priority,
                                                    description=description,
                                                    created=now
                                                    )
            self.db_session.add(profile_pricing)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.db_session.refresh(profile_pricing)
            return profile_pricing
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: profile_pricing_object.py method: create_default fail {e}")
            raise e
    
    def get_lower_priority_profile(self) -> float|None:
        try:
            profile_pricing:ModelPricingProfile = self.db_session.query(ModelPricingProfile).order_by(ModelPricingProfile.priority.asc()).first()
            if not profile_pricing:
                return None
            return profile_pricing.priority
        except Exception:
            return None
        
    def get_next_lower_priority(self, priority_base: float |None, current_next_lower: float = None) -> float:
        """
        Returns the next lower priority from the base priority within the range of the next lower priority.
        
        Args:
            priority_base (float): The base priority.
            priority_next_lower (float): The lower limit of the range to search for the next lower priority.
            
        Returns:
            float: The next lower priority within the specified range.
            """
        if not priority_base:
            return 0
        if not current_next_lower:
            return priority_base - 0.1
        
        if current_next_lower:
            # return the  more higher number between the current next lower and the base priority
            return max(current_next_lower, priority_base - 0.1)
        
    def get_next_higher_priority(self, priority_base: float = 0, current_next_higher: float = None) -> float:
        
        """
        Returns the next higher priority from the base priority within the range of the next higher priority.
        
        Args:
            priority_base (float): The base priority.
            priority_next_higher (float): The higher limit of the range to search for the next higher priority.
            
        Returns:
            float: The next higher priority within the specified range.
        """
        if not current_next_higher:
            return priority_base + 0.1
        
        if current_next_higher:
            # return the more lower number between the current next higher and the base priority
            return min(current_next_higher, priority_base + 0.1)    
    
    def delete(self, id: int, auto_commit: bool = True):
        return super().delete(id, auto_commit)
    
    def delete_all(self, auto_commit: bool = True) -> None:
        return super().delete_all(auto_commit)