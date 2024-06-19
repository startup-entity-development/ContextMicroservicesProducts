import logging
from typing import List
from flask import request
import graphene
from pricing_ctx_database_sqlalchemy_14.models.model_pricing_account import ModelPricingAccount
from pricing_ctx_database_sqlalchemy_14.models.model_pricing_profile import ModelPricingProfile
from nodes.cart_pricing_calculation import CartPricingCalculation
from resources.account_pricing_functions import AccountPricingFunctions
from resources.promotion_functions import AccountPromotionFunctions

class ResolversAccountPricingCart:
    
    """
    Resolvers for the account pricing cart.
    """

    cart_pricing_calculation = graphene.Field(CartPricingCalculation, 
                                            sub_total = graphene.Float(description="Subtotal of the cart", required=True),
                                            total_pounds = graphene.Float(description="Total pounds", default_value=0, required=False),
                                            coupon_codes =  graphene.List(graphene.String, description="Coupon codes", required=False),
                                            tips = graphene.Float(  description="Tips",
                                                                    default_value=0,
                                                                    required=False))
    
    def resolve_cart_pricing_calculation(self, info, sub_total:float, coupon_codes:List, total_pounds:float, tips:float):
        account_name = request.headers.get('X-Auth-User') #TODO : Change this to the external account id
        
        #TODO: get role and level using account_name, in this stage only the default profile is used
        role_name:str|None = None
        level_name:str|None = None
        query = CartPricingCalculation.get_query(info)    
        current_pricing_account = query.filter(ModelPricingAccount.external_account_id == account_name).first()
        if not current_pricing_account:
            accountPricingFunctions:AccountPricingFunctions = AccountPricingFunctions(external_account_id=account_name) 
            pricing_profile:ModelPricingProfile = accountPricingFunctions.obtain_pricing_profile(rule_name=role_name, level_name=level_name)
            current_pricing_account:ModelPricingAccount = accountPricingFunctions.assign_pricing_profile(pricing_profile)
        
        accountPromotionFunctions:AccountPromotionFunctions = AccountPromotionFunctions(account_pricing_id=current_pricing_account.id)
        
        if coupon_codes:
            for coupon in coupon_codes:
                accountPromotionFunctions.add_promotion_by_coupon_code(coupon_code=coupon)
        
        current_pricing_account = query.filter(ModelPricingAccount.external_account_id == account_name).first()
        return current_pricing_account
        


