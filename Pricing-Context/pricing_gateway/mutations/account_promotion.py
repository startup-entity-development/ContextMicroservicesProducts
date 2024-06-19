import logging
import time
import graphene
from graphql_relay import from_global_id
from pricing_ctx_database_sqlalchemy_14.models.base import db_session
from pricing_ctx_database_sqlalchemy_14.objects.account_promotion_object import AccountPromotionDataBase

class UpdateCounterAccountPromotion(graphene.Mutation):
    counter_uses = graphene.Int(description="New counter value")
    available_usage_times = graphene.Int(description="Times of use")
    account_promotion_continues_active = graphene.Boolean(description="If the promotion continue active for this account")
    
    class Arguments:
        account_promotion_id = graphene.ID(description="Account Promotion Id", required=True)
        increase_value = graphene.Int(description="Set value of counter", required=False, default_value=1)
        

    def mutate(self, info, account_promotion_id:str, increase_value:int) -> "UpdateCounterAccountPromotion":
        
        """
        if the promo use reach the limit of times of use, the promotion is deactivated
        """
        log = logging.getLogger(__name__)
        account_promotion_id:int = int(from_global_id(account_promotion_id).id)
        account_promotion_database: AccountPromotionDataBase = AccountPromotionDataBase(db_session=db_session,
                                                                                        log= log)
        account_promotion = account_promotion_database.get(id=account_promotion_id)
        now = int(time.time())
        if account_promotion.promotion.start_timestamp > now:
            raise Exception(f"The promotion is not active yet, error_code: $UCAP000, account_promotion_id = {account_promotion_id}, promotion_id = {account_promotion.promotion.id}")
        if account_promotion.promotion.end_timestamp < now:
            raise Exception(f"The promotion is ended, error_code: $UCAP001, id database = {account_promotion_id}, promotion_id = {account_promotion.promotion.id}")
        if account_promotion.promotion.is_active is False:
            raise Exception(f"The promotion is not active, error_code: $UCAP002, id database = {account_promotion_id}, promotion_id = {account_promotion.promotion.id}")
    
        if account_promotion.is_active is False:
            raise Exception(f"The promotion for this account is not active, error_code: $UCAP003, id database = {account_promotion_id}")
        # sure that the new value is not greater than the times_of_use and positive
        if increase_value < 0:
            raise Exception(f"Value to increase must be positive, error_code: $UCAP004, id database = {account_promotion_id}")
        
        if account_promotion.promotions_counter + increase_value > account_promotion.promotion.times_of_use:
            raise Exception(f"Value to increase is greater than the times of use, error_code: $UCAP005, id database = {account_promotion_id}")
        
        account_promotion.promotions_counter += increase_value
        account_promotion.updated = now
        if account_promotion.promotions_counter >= account_promotion.promotion.times_of_use:
            account_promotion.is_active = False
        db_session.add(account_promotion)
        db_session.commit()
        return UpdateCounterAccountPromotion(
            counter_uses = account_promotion.promotions_counter,
            available_usage_times = account_promotion.promotion.times_of_use - account_promotion.promotions_counter,
            account_promotion_continues_active = account_promotion.is_active
        )
        
        
class MutationsAccountPromotion():
    update_counter_promotion = UpdateCounterAccountPromotion.Field()

        