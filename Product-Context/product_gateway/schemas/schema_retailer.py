
from graphene_sqlalchemy import SQLAlchemyConnectionField
from nodes.retailer import Retailer

class ResolversRetailer:
    # Product
    retailer_list = SQLAlchemyConnectionField(Retailer.connection)

class ResolversRetailerPublic:
    # Product
    """"
    Retailer Public
    """