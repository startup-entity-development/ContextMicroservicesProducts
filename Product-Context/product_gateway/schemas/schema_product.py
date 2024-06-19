from api_integrations.barcodelookup.get_product_by_upc_code import ProductBarcodeLookup
from product_ctx_database_sqlalchemy_14.models.media_model import ModelMedia
from product_ctx_database_sqlalchemy_14.models.product_model import ModelProduct
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphql_relay.node.node import from_global_id
from sqlalchemy import func
import graphene
import re
from product_ctx_database_sqlalchemy_14.models.product_retailer_model import ModelProductRetailer
from mutations.create_product import CreateProduct
from mutations.update_product import UpdateProduct
from nodes.product_media import Product
from sqlalchemy import case, or_



def get_offset(page:int , limit_result:int)->int:
    offset = 0
    for i in range(page):
        offset = offset + limit_result
    return offset    

class ResolversProduct:
    # Product
    product_list = SQLAlchemyConnectionField(Product.connection)
    product_by_id = graphene.Field(Product, product_id=graphene.ID(required=True))
    
    products_by_list_ids = graphene.List(Product, list_id=graphene.List(graphene.ID, required=True))
    
    product_by_upc = graphene.Field(Product, upc_barcode=graphene.String(required=True))
    
    product_by_subcategory_id = SQLAlchemyConnectionField(Product, 
                                                          id=graphene.ID(required=True),
                                                          limit_result=graphene.Int(),
                                                          offset=graphene.Int(),
                                                          only_active=graphene.Boolean( required=False,
                                                           default_value=True))
    
    finder_product = SQLAlchemyConnectionField(Product,
                                               to_find=graphene.String(),
                                               limit_result=graphene.Int(),
                                               offset=graphene.Int(),
                                               only_active=graphene.Boolean( required=False,
                                               default_value=True))
   
   

    
    def resolve_finder_product(root, context,
                               to_find,
                               limit_result:int=30,
                               offset:int=0,
                               only_active:bool=True):
        
        offset = get_offset(offset, limit_result)
        if to_find == "- ":
            to_find = "org"
        to_find = to_find.lower()
       
        to_find = re.sub(r'[^\w\s]', ' ', to_find)
        to_find = re.sub(' +', ' ', to_find)
        to_find = to_find.strip()
        to_find = re.sub(' +', ' ', to_find)
        
        to_find = to_find.replace(" ", " & ")
        to_find = to_find.replace(":", "")
        
        if len(to_find) < 1:
            return []
            
        #tsquery = func.plainto_tsquery("english", to_find)
        # stmt = select(ModelProduct).where(
        #     ModelProduct.title_tsv.bool_op("@@")(tsquery)
        # )
        # query_result = db_session.execute(stmt).scalars().all()
        # remove symbols in to_find
        
        to_find = to_find + ":*"
        query_result = ModelProduct.query\
            .filter(ModelProduct.is_active == only_active)\
            .filter(or_(ModelProduct.words_tags_tsv.match(to_find),
                    ModelProduct.brand_tsv.match(to_find),
                     ModelProduct.title_tsv.match(to_find)))\
            .order_by(case([(ModelProduct.words_tags_tsv.match(to_find), 1)], else_=2))\
            .order_by(func.length(ModelProduct.title))\
            .limit(limit_result)\
            .offset(offset).all()

        return query_result
    
    
    def resolve_product_by_upc(root, context, upc_barcode):
        try: 
            query = Product.get_query(context)       
            query_result = query.filter(ModelProduct.upc_barcode == upc_barcode).first()
            
            if query_result:
                return query_result
            else:
                productBarcodeLookup = ProductBarcodeLookup()
                product_attributes = productBarcodeLookup.get_product_attributes(upc_barcode)
                size = product_attributes.size
                title = product_attributes.title
                
                if size == None: size = ""
                if size != "": title = f"{title} - {size}"
                
                model_product = ModelProduct(id="is_not_in_db",
                                            sub_category_id="is_not_in_db",
                                            api_id=None,
                                            name=product_attributes.title,
                                            title=title,
                                            words_tags="",
                                            brand=product_attributes.brand,
                                            base_increment=1,
                                            description=product_attributes.description,
                                            upc_barcode=product_attributes.barcode_number,
                                            unit_measure=None,
                                            weight=None,
                                            size=size,
                                            unit_in_pack=None,
                                            dpci=None,
                                            tcin=None)
                list_model_media = []
                
                for image_url in product_attributes.images:
                    is_main = False
                    if image_url == product_attributes.images[0]:
                        is_main = True
                    model_media = ModelMedia(id=None,
                                            product_id=None,
                                            link_url=image_url,
                                            is_main=is_main)
                    list_model_media.append(model_media)
                
                model_product.media_edge = list_model_media

                model_retailer = ModelProductRetailer(id="is_not_in_db",
                                            product_id="is_not_in_db",
                                            retailer_id="is_not_in_db",
                                            cost=0.0,
                                            increment_retailer=1,
                                            stock=1,
                                            is_active=True,
                                            is_in_stock=True,)

                model_product.retailer_edge = [model_retailer]

                query_result = model_product

        except Exception as e:
            raise Exception(f"Error in product_by_upc: {e}, error_code: $RPBUNIDB002")
        return query_result
    
    def resolve_product_by_subcategory_id(root, context, id, limit_result:int=30, offset:int=0, only_active:bool=True):
        offset = get_offset(offset, limit_result)
        
        id_subcategory = int(from_global_id(id).id)
        query = Product.get_query(context)       
        
        query_result = query.filter(ModelProduct.sub_category_id == id_subcategory, 
        ModelProduct.is_active == only_active).limit(limit_result).offset(offset).all()
        return query_result
    
    def resolve_product_by_id(root, context, product_id):        
        id_product = int(from_global_id(product_id).id)
        query = Product.get_query(context)   
            
        query_result = query.filter(ModelProduct.id == id_product).first()
        if not query_result:
            raise Exception(f"Product not found, id: {product_id}, error_code: $RPBI0001")
        return query_result
    
    def resolve_products_by_list_ids(root, context, list_id):
        
        list_id_product = []
        try:
            for id in list_id:
                list_id_product.append(int(from_global_id(id).id))
        except Exception as e:
            raise Exception(f"Error in decode the list_id: {e}, error_code: $RPBI0002")
        query = Product.get_query(context)   
    
        query_result = query.filter(ModelProduct.id.in_(list_id_product)).all()
        return query_result
    

class MutationProduct:
    createProduct = CreateProduct.Field()
    updateProduct = UpdateProduct.Field()
