import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from product_ctx_database_sqlalchemy_14.models.category_model import ModelCategory
from product_ctx_database_sqlalchemy_14.models.sub_category_model import ModelSubCategory
from graphql_relay.node.node import from_global_id

class Category(SQLAlchemyObjectType):
    class Meta:
        model = ModelCategory
        interfaces = (graphene.relay.Node,)

class SubCategory(SQLAlchemyObjectType):
    class Meta:
        model = ModelSubCategory
        interfaces = (graphene.relay.Node, )
    
class ResolversCategory:
    # Category
    category_list = SQLAlchemyConnectionField(Category.connection)
    get_category = graphene.Field(Category, id=graphene.ID(required=True))
    get_category_by_name = graphene.Field(Category, name_category=graphene.String(required=True))

    def resolve_get_category(root, context, id):
        id_category = int(from_global_id(id).id)
        query = Category.get_query(context)       
        category = query.filter(ModelCategory.id == id_category).first()
        return category
    
    def resolve_get_category_by_name(root, context, name_category):
        query = Category.get_query(context)       
        category = query.filter(ModelCategory.name == name_category).first()
        return category
    
class ResolversSubCategory:
    """
    Resolvers for SubCategory GraphQL queries and mutations.
    """

    subcategory_list = SQLAlchemyConnectionField(SubCategory.connection)
    get_subcategory = graphene.Field(SubCategory, id=graphene.ID(required=True))
    get_subcategory_by_name = graphene.Field(SubCategory, name_subcategory=graphene.String(required=True))

    def resolve_get_subcategory(root, context, id):
        """
        Resolve the 'get_subcategory' query by ID.

        Args:
            root: The root resolver object.
            context: The GraphQL context.
            id: The ID of the subcategory.

        Returns:
            The subcategory with the specified ID.
        """
        id_subcategory = int(from_global_id(id).id)
        query = SubCategory.get_query(context)       
        subcategory = query.filter(ModelSubCategory.id == id_subcategory).first()
        return subcategory
    
    def resolve_get_subcategory_by_name(root, context, name_subcategory):
        """
        Resolve the 'get_subcategory_by_name' query by name.

        Args:
            root: The root resolver object.
            context: The GraphQL context.
            name_subcategory: The name of the subcategory.

        Returns:
            The subcategory with the specified name.
        """
        query = SubCategory.get_query(context)       
        sub_category = query.filter(ModelSubCategory.name == name_subcategory).first()
        return sub_category
    

