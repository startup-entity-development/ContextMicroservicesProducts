import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from order_ctx_database_sqlalchemy_14.models.cart_product_detail import ModelCartProductDetail
from graphql_relay.node.node import from_global_id, to_global_id
from services.product_service import resolve_getProductById

class UnitOfMeasure(graphene.Enum):
    ounce = "ounce"
    pound = "pound"
    kilo = "kilo"
    gram = "gram"
    liter = "liter"
    gallon = "gallon"
    milliliter = "milliliter"

class MediaSchema(graphene.ObjectType):
    id = graphene.ID(required=True)
    linkUrl = graphene.String(required=True)
    isMain = graphene.Boolean(required=True)
    mediaType = graphene.String(required=True)

class ProductRetailerSchema(graphene.ObjectType):
    id = graphene.ID(description= "Id of the Retailer", required=True)
    retailerId = graphene.ID(description= "Id of the Retailer", required=True)
    productId = graphene.ID(description= "Id of the Product", required=True)
    linkUrl = graphene.String(description= "Link of the Retailer", required=True)
    price = graphene.Float(description= "Cost of the Product", required=True)    
    incrementRetailer = graphene.Float(description= "Increment based in the retailer", required=False)
    stock = graphene.Int(description= "Stock of the Product", required=False)
    isActive = graphene.Boolean(description= "Status of the Product", required=False)
    isInStock = graphene.Boolean(description= "Status of the Product", required=False)

class MediaConnection(graphene.Connection):

    class Meta:
        node = MediaSchema
    
class ProductRetailerConnection(graphene.Connection):
    
        class Meta:
            node = ProductRetailerSchema
            
class ProductSchema(graphene.ObjectType):
    id = graphene.ID(required=True)
    upcBarcode = graphene.String(description= "UpcBarcode of the Product.", required=True)
    subCategoryId = graphene.ID(description= "Id of the SubCategory", required=True)
    title = graphene.String(description= "Title of the Product", required=True)
    size = graphene.String(description= "Size of the Product", required=False, default_value=None)
    brand = graphene.String(description= "Brand of the Product", required=True)
    description = graphene.String(description= "Description of the Product", required=True)

    #new options fields product
    wordsTags = graphene.String(description= "TagsWords of the Product", required=False, default_value=None)
    weight = graphene.Float(description= "Weight of the Product", required=False, default_value=None)
    unitMeasure = UnitOfMeasure(description= "Unit of Measure of the Product", required=False, default_value=None)
    baseIncrement = graphene.Float(description= "Product Base Increment of the Product", required=False, default_value=None)
    unitInPack = graphene.Int(description= "Unit in Pack of the Product", required=False, default_value=None)
    isActive = graphene.Boolean(description= "Status of the Product", required=False, default_value=True)
    mediaEdge = graphene.ConnectionField(MediaConnection)
    retailerEdge = graphene.ConnectionField(ProductRetailerConnection)


class CartProductDetailSchema(SQLAlchemyObjectType):
    product = graphene.Field(ProductSchema)
    
    class Meta:
        model = ModelCartProductDetail
        interfaces = (graphene.relay.Node,)

class CartProductDetailResolver:
    # CartProductDetailSchema
    cart_product_detail_list = SQLAlchemyConnectionField(CartProductDetailSchema.connection)
    get_cart_product_detail = graphene.Field(CartProductDetailSchema, id=graphene.ID(required=True))

    def resolve_get_cart_product_detail(root, context, id):
        id_cart_product_detail = int(from_global_id(id).id)
        query = CartProductDetailSchema.get_query(context)       
        cart_product_detail = query.filter(ModelCartProductDetail.id == id_cart_product_detail).first()

        global_product_id = to_global_id("Product", cart_product_detail.product_id)
        product = resolve_getProductById(global_product_id)
        cart_product_detail.product = product
        return cart_product_detail