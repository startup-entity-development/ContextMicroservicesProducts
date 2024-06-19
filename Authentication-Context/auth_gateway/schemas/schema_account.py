import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphql_relay import from_global_id
from account_management.mutation_create_account import AccountExclude, CreateAccount
from authentication_management.mutation_authentication_private import ProtectedSoftDeleteAccount
from authentication_management.mutation_authentication_public import LoginAccount
from authorization_management.mutation_assign_role_level import AssignRoleLevel
from authorization_management.authorization_middleware import require_permission_internal

class PublicAccountResolvers:
    
    account_by_id = graphene.Field(AccountExclude, id=graphene.ID(required=True))

    def resolve_account_by_id(root, context, id):
        query = AccountExclude.get_query(context)
        account_id:int = int(from_global_id(id).id)
        query_result = query.filter(AccountExclude.id == account_id).first()
        return query_result


class ProtectedAccountResolvers:
    accounts = SQLAlchemyConnectionField(AccountExclude)



    @require_permission_internal(root_user=True)
    def resolve_accounts(root, context ):
        query = AccountExclude.get_query(context)
        query_result = query.all()
        return query_result



    
class PublicAccountMutations:
    createAccount = CreateAccount.Field()
    loginAccount = LoginAccount.Field()

class ProtectedAccountMutations:
    softDeleteAccount = ProtectedSoftDeleteAccount.Field()

class ProtectedAuthorizationMutations:
    assign_role_level = AssignRoleLevel.Field()
    

    