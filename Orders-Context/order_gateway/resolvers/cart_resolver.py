from ast import Dict
from flask import request
import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from order_ctx_database_sqlalchemy_14.models.cart import ModelCart
from resolvers.cart_product_detail_resolver import CartProductDetailSchema, ProductSchema
from graphql_relay.node.node import from_global_id, to_global_id
from services.product_service import resolve_getProductsByIds
from services.pricing_service import resolve_cartPricingCalculation

class TypePromotion(graphene.Enum):
    percent = "percent"
    amount = "amount"
    
class deliveryFee(graphene.ObjectType):
    deliveryFee = graphene.Float(description="Delivery fee", default_value=0)
    discountDelivery = graphene.Float(description="Discount, default value 0", default_value=0)
    typePromotion = TypePromotion(description="Type of promotion", default_value= TypePromotion.amount.value)
    totalDelivery = graphene.Float(description="Total promotion", default_value=0)
    idPromotion = graphene.ID(description="Id of the promotion", required=False)
    idAccountPromotion = graphene.ID(description="Id of the account promotion", required=False)

    def resolve_typePromotion(self, info):
        type_promotion:str = self["typePromotion"].lower()
        return type_promotion

class serviceFee(graphene.ObjectType):
    serviceFee = graphene.Float(description="Service fee", default_value=0)
    discountService = graphene.Float(description="Discount", default_value=0)
    typePromotion = TypePromotion(description="Type of promotion", default_value= TypePromotion.amount.value)
    totalService = graphene.Float(description="Total service", default_value=0)
    idPromotion = graphene.ID(description="Id of the promotion", required=False)
    idAccountPromotion = graphene.ID(description="Id of the account promotion", required=False)
    
class accountPromotion(graphene.ObjectType):
    id = graphene.ID(description="ID of the account promotion", default_value=0)
    isActive = graphene.Boolean(description="Is active", default_value=False)
    promotionsCounter = graphene.Int(description="Promotions counter", default_value=0)
    
    def resolve_id(self, info):
        return self["id"]

class accountPromotionEdge(graphene.Connection):
    
    class Meta:
        node = accountPromotion
    
    def resolve_edges(self, info):
        return self.edges
    
class CartPricingCalculationSchema(graphene.ObjectType):

    subTotal = graphene.Float(description="Subtotal of the cart", default_value=0)
    deliveryService = graphene.Field(deliveryFee, description="Delivery")
    serviceFee = graphene.Field(serviceFee, description="Service")
    minimumSubtotal = graphene.Float(description="Minimum subtotal", default_value=0)
    tips = graphene.Float(description="Tips", default_value=0)
    tax = graphene.Float(description="Tax percent", default_value=0)
    taxPercent = graphene.Float(description="Tax percent", default_value=0)
    total = graphene.Float(description="Total of the cart", default_value=0)


class CartSchema(SQLAlchemyObjectType):

    cartProductsEdge = SQLAlchemyConnectionField(CartProductDetailSchema)
    pricingCalculation = graphene.Field(CartPricingCalculationSchema, description="Pricing calculation")
    #accountPromotionEdge = graphene.ConnectionField(accountPromotionEdge, description="Account promotion")
    class Meta:
        model = ModelCart
        interfaces = (graphene.relay.Node,)

    def resolve_cartProductsEdge(self, info):
        
        cart_products = [cart_product for cart_product in self.cart_products_edge  if cart_product.quantity > 0]
        product_ids = [to_global_id("Product", cart_product.product_id) for cart_product in cart_products]
        
        if len(product_ids):
            products_data = resolve_getProductsByIds(product_ids=product_ids)
            products = {}
            
            for product in products_data:
                product_id = from_global_id(product["id"]).id
                mediaEdge = []
                mediaDict = {}
                retailerEdge = []
                retailerDict = {}
                if product_id:
                    products[int(product_id)] = product
                    mediaList = product["mediaEdge"]["edges"]
                    retailerList = product["retailerEdge"]["edges"]
                    for retailer in retailerList:
                        retailerDict = retailer["node"]
                        retailerEdge.append(retailerDict)
                    for media in mediaList:
                        mediaDict = media["node"]
                        mediaEdge.append(mediaDict) 
                    products[int(product_id)]["mediaEdge"] = mediaEdge
                    products[int(product_id)]["retailerEdge"] = retailerEdge
    
            for cart_product in cart_products:
                product = products.get(cart_product.product_id, None)
                if product:
                    cart_product.product = product

        return cart_products
    
    def resolve_pricingCalculation(self, info):
        product_sub_total = 0
        total_pounds = 0
        cart_products = [cart_product for cart_product in self.cart_products_edge  if cart_product.quantity > 0]

        for cart_product in cart_products:
            product_sub_total += cart_product.price * cart_product.quantity 
            # TODO: Next Integration TOTAL POUNDS
            # add weight pounds in product_detail_node
            # get this in the mutation product_detail_mutation

        pricing_calculation = resolve_cartPricingCalculation(sub_total=product_sub_total, total_pounds=0)
        return pricing_calculation

class CartResolver:
    # Cart
    cart_list = SQLAlchemyConnectionField(CartSchema.connection)
    get_cart = graphene.Field(CartSchema, id=graphene.ID(required=True))
    get_cart_last_order = graphene.List(CartSchema)

    def resolve_get_cart(root, context, id):
        id_cart = int(from_global_id(id).id)
        query = CartSchema.get_query(context)       
        cart = query.filter(ModelCart.id == id_cart).first()
        return cart
    
    def resolve_get_cart_last_order(root, context):
        query = CartSchema.get_query(context)    
        user_account_id = int(request.headers.get('X-Auth-Id'))   
        cart = query\
            .filter_by(user_account_id = user_account_id)\
            .filter(ModelCart.deactive_date != None)\
            .order_by(ModelCart.id.desc())\
            .limit(1)\
            .offset(0).all()
        
        return cart
