import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from pricing_ctx_database_sqlalchemy_14.models.model_pricing_account import ModelPricingAccount
from pricing_ctx_database_sqlalchemy_14.models.model_pricing_profile import ModelPricingProfile

class PricingAccount(SQLAlchemyObjectType):
    class Meta:
        model = ModelPricingAccount
        interfaces = (graphene.relay.Node,)

class PricingProfile(SQLAlchemyObjectType):
    class Meta:
        model = ModelPricingProfile
        interfaces = (graphene.relay.Node,)