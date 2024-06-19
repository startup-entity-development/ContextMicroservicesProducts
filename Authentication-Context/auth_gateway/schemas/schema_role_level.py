
import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from graphql_relay import from_global_id
from account_management.mutation_create_account import Account, AccountExclude, CreateAccount
from auth_model_sqlalchemy_14.account_role_level import ModelAccountRoleLevel
from auth_model_sqlalchemy_14.level import ModelLevel
from auth_model_sqlalchemy_14.role import ModelRole
from authorization_management.mutation_create_role_level import CreateLevel, CreateRole
from authorization_management.authorization_middleware import require_permission_internal

class Role(SQLAlchemyObjectType):
    class Meta:
        model = ModelRole
        interfaces = (graphene.relay.Node, )


class Level(SQLAlchemyObjectType):
    class Meta:
        model = ModelLevel
        interfaces = (graphene.relay.Node, )

class AccountRoleLevel(SQLAlchemyObjectType):
    class Meta:
        model = ModelAccountRoleLevel
        interfaces = (graphene.relay.Node, )



class ProtectedRoleResolvers:
    # Account
    roles = SQLAlchemyConnectionField(Role)
    
    @require_permission_internal(root_user=True)
    def resolve_roles(root, context ):
        query = Role.get_query(context)
        query_result = query.all()
        return query_result

class ProtectedLevelResolvers:
    # Account
    levels = SQLAlchemyConnectionField(Level)
    
    @require_permission_internal(root_user=True)
    def resolve_levels(root, context ):
        query = Level.get_query(context)
        query_result = query.all()
        return query_result

    
class ProtectedMutationsRole:

    createRole = CreateRole.Field()    

class ProtectedMutationLevel:

    createLevel = CreateLevel.Field()

