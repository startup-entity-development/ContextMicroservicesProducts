
import logging
import time
from typing import List
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from pricing_ctx_database_sqlalchemy_14.models.model_account_promotion import ModelAccountPromotion
from pricing_ctx_database_sqlalchemy_14.models.model_pricing_account import ModelPricingAccount
from pricing_ctx_database_sqlalchemy_14.models.model_promotion import ModelPromotion
from pricing_ctx_database_sqlalchemy_14.objects.promotion_object import TypePromotion, WhereApplies
from pricing_ctx_database_sqlalchemy_14.models.base import db_session
from nodes.account_pricing import  PricingProfile
from sqlalchemy import and_
from resources.delivery_fee import DeliveryFeeBasedInWight
from graphql_relay.node.node import to_global_id

delivery_wight = DeliveryFeeBasedInWight(log = logging.getLogger(__name__), db_session = db_session)



class Promotion(SQLAlchemyObjectType):

    class Meta:
        model = ModelPromotion
        interfaces = (graphene.relay.Node,)
        exclude_fields = (  "rule_access_name",
                            "level_access_name",)

class AccountPromotion(SQLAlchemyObjectType):
    promotion = graphene.Field(lambda: Promotion, description="Promotion")
    class Meta:
        model = ModelAccountPromotion
        interfaces = (graphene.relay.Node,)
        
class deliveryFee(graphene.ObjectType):
    delivery_fee = graphene.Float(description="Delivery fee", default_value=0)
    discount_delivery = graphene.Float(description="Discount", default_value=0)
    type_promotion = TypePromotion(description="Type of promotion", default_value= TypePromotion.amount.value)
    total_delivery = graphene.Float(description="Total delivery", default_value=0)
    id_promotion = graphene.ID(description="Id of the promotion", required=False)
    id_account_promotion = graphene.ID(description="Id of the account promotion", required=False)

class serviceFee(graphene.ObjectType):
    service_fee = graphene.Float(description="Service fee", default_value=0)
    discount_service = graphene.Float(description="Discount", default_value=0)
    type_promotion = TypePromotion(description="Type of promotion", default_value= TypePromotion.amount.value)
    total_service = graphene.Float(description="Total service", default_value=0)
    id_promotion = graphene.ID(description="Id of the promotion", required=False)
    id_account_promotion = graphene.ID(description="Id of the account promotion", required=False)

# class productPromotions(graphene.ObjectType):
#     id_product = graphene.ID(description="Id of the product", required=False)
#     id_subcategory = graphene.ID(description="Id of the subcategory", required=False)
#     discount_product = graphene.Float(description="Discount", default_value=0)
#     type_promotion = TypePromotion(description="Type of promotion", default_value= TypePromotion.amount.value)
#     id_promotion = graphene.ID(description="Id of the promotion", required=False)
#     id_account_promotion = graphene.ID(description="Id of the account promotion", required=False)
#     coupon_code = graphene.String(description="Coupon code", required=True)


def get_valid_account_promotions(self, info, **kwargs):
        query = AccountPromotion.get_query(info)
        print(self)
        list_account_promotion:List[ModelAccountPromotion] =query.filter(and_(ModelAccountPromotion.id_account_pricing == self.id, ModelAccountPromotion.is_active == True)).all()
        # crate a new list where the promo is active, not expired and times_of_use is less than promotion_counter
        now_timestamp:int = int(time.time())

        new_list_account_promotion = []
        for account_promotion in list_account_promotion:
            if account_promotion.promotion.is_active and \
                account_promotion.promotion.start_timestamp < now_timestamp and\
                account_promotion.promotion.end_timestamp > now_timestamp and\
                    account_promotion.promotions_counter < account_promotion.promotion.times_of_use:
                new_list_account_promotion.append(account_promotion)
        return  new_list_account_promotion

def get_delivery_service(self, info, **kwargs):
    list_account_promotions = get_valid_account_promotions(self, info, **kwargs)
    only_delivery_fee = [account_promotion for account_promotion in list_account_promotions if account_promotion.promotion.where_applies == WhereApplies.delivery_fee.value]
    deliveryFee.delivery_fee = self.pricing_profile.delivery_fee_base 
    #if only_delivery_fee has more that one promotion, the last one is the one that will be applied use the id to sort
    only_delivery_fee.sort(key=lambda x: x.promotion.id, reverse=True)
    delivery_fee_weight = delivery_wight.get_delivery_fee(self.pricing_profile.delivery_fee_base, 11)

    if not delivery_fee_weight:
        delivery_fee_weight = self.pricing_profile.delivery_fee_base
    
    last_promotion = None

    if only_delivery_fee:
        last_promotion = only_delivery_fee[0]
    
    if not last_promotion:
        return deliveryFee(
            delivery_fee = self.pricing_profile.delivery_fee_base,
            discount_delivery = 0,
            type_promotion = TypePromotion.amount.value,
        )
    
    discount_delivery:int = 0

        
    if last_promotion.promotion.where_applies == WhereApplies.delivery_fee.value:
        if last_promotion.promotion.type_promotion == TypePromotion.amount.value:
            discount_delivery = last_promotion.promotion.value_amount
            total_delivery = delivery_fee_weight - discount_delivery
        elif last_promotion.promotion.type_promotion == TypePromotion.percent.value:
            discount_delivery = last_promotion.promotion.value_percent
            total_delivery = delivery_fee_weight - (delivery_fee_weight / 100 * discount_delivery)

    if delivery_fee_weight < 0:
        delivery_fee_weight = 0

    if total_delivery < 0:
        total_delivery = 0
        
    if isinstance(total_delivery, int):
        total_delivery = total_delivery - 0.01
    
    if isinstance(delivery_fee_weight, float):
        delivery_fee_weight = delivery_fee_weight - 0.01
        
        
        return deliveryFee(
        delivery_fee = round(delivery_fee_weight, 2),
        discount_delivery = round(discount_delivery, 2),
        type_promotion = last_promotion.promotion.type_promotion,
        total_delivery = round(total_delivery, 2),
        id_promotion = to_global_id("promotion_id", last_promotion.promotion.id),
        id_account_promotion = to_global_id("account_promotion_id",last_promotion.id)

    )
    
def get_total_delivery_service(self, info, **kwargs) -> float:
    delivery_service:deliveryFee = get_delivery_service(self, info, **kwargs)
    if delivery_service.type_promotion == TypePromotion.amount.value:
        delivery_total = delivery_service.delivery_fee - delivery_service.discount_delivery
        if delivery_total < 0:
            delivery_total = 0
        return delivery_total
    if delivery_service.type_promotion == TypePromotion.percent.value:
        delivery_total = delivery_service.delivery_fee - (delivery_service.delivery_fee / 100 * delivery_service.discount_delivery)
        if delivery_total < 0:
            delivery_total = 0
        return delivery_total
    return 0
    
class CartPricingCalculation(SQLAlchemyObjectType):

    sub_total = graphene.Float(description="Subtotal of the cart", default_value=0)
    deliveryService = graphene.Field(deliveryFee, description="Delivery")
    serviceFee = graphene.Field(serviceFee, description="Service")
    minimum_subtotal = graphene.Float(description="Minimum subtotal", default_value=0)
    tips = graphene.Float(description="Tips", default_value=0)
    tax = graphene.Float(description="Tax percent", default_value=0)
    tax_percent = graphene.Float(description="Tax percent", default_value=0)
    total = graphene.Float(description="Total of the cart", default_value=0)
    
    account_promotion_edge = graphene.ConnectionField(AccountPromotion.connection, description="Account Promotion edge")
    pricing_profile = graphene.Field(lambda: PricingProfile, description="Account pricing SQLAlchemyObjectType" )
    
    class Meta:
        model = ModelPricingAccount
        interfaces = (graphene.relay.Node,)
    
    def resolve_deliveryService(self, info,**kwargs):
        return get_delivery_service(self, info, **kwargs)
        
        
    def resolve_sub_total(self, info, **kwargs):
        sub_total = info.variable_values.get('subTotal')
        return sub_total
    
    def resolve_minimum_subtotal(self, info, **kwargs):
        return  self.pricing_profile.minimum_subtotal 
    
    def resolve_tips(self, info, **kwargs):
        tips = info.variable_values.get('tips', 0)
        return  tips
    
    def resolve_tax(self, info, **kwargs):
        sub_total = info.variable_values.get('subTotal')
        if not sub_total:
            return 0
        tax_percent =  self.pricing_profile.tax 
        return sub_total / 100 * tax_percent
    
    def resolve_tax_percent(self, info, **kwargs):
        return self.pricing_profile.tax
    
    def resolve_total(self, info, **kwargs):
        sub_total = info.variable_values.get('subTotal')
        tips = info.variable_values.get('tips', 0)
        tax_percent =  self.pricing_profile.tax 
        tax = 0
        if sub_total:
            tax = sub_total / 100 * tax_percent
        total_delivery_service = get_total_delivery_service(self,info, **kwargs)
        return sub_total + tips + tax + total_delivery_service

    def resolve_account_promotion_edge(self, info, **kwargs):
        # filter where is_active = False
        return get_valid_account_promotions(self, info, **kwargs)