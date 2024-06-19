from typing import Dict
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql_relay import from_global_id
from account_management.account_functions import AccountFuntions
from account_management.mutation_create_account import Account
from auth_model_sqlalchemy_14.account_role_level import ModelAccountRoleLevel
from authorization_management.authorization_functions import AuthorizationFuntions
from auth_model_sqlalchemy_14.base import db_session


class AccountRoleLevel(SQLAlchemyObjectType):
    """Account node."""

    class Meta:
        model = ModelAccountRoleLevel
        interfaces = (graphene.relay.Node,)
 
class AssignRoleGraphAttribute:
    account_id = graphene.ID(description="Account ID.", required=True)
    role_name = graphene.String(description="Role Name.", required=True)
    level_name = graphene.String(description="Level Name.", required=True)



class AssignRoleGraphInput(graphene.InputObjectType, AssignRoleGraphAttribute):
    """Arguments to create a account."""
    pass

class AssignRoleLevel(graphene.Mutation):
    """Mutation to create a account."""

    account_role_level = graphene.Field(
        lambda: AccountRoleLevel, description="AccountRoleLevel created by this mutation."
    )
   

    class Arguments:
       input = AssignRoleGraphInput(required=True)

    
    def mutate(self, context, input:Dict):
        
        account_id = input.get('account_id')
        role_name = input.get('role_name')
        level_name = input.get('level_name')
        
        try:    
            decode_account_id = int(from_global_id(account_id).id)
        except Exception as e:
            raise Exception(f"|$ARL1000 - Error to decode account id: {account_id}")
        
        accountFunctions:AccountFuntions = AccountFuntions(session=db_session)

        account = accountFunctions.get_account_by_id(account_id=decode_account_id)
        
        if account is None:
            raise Exception(f"|$ARL1001 - Error to get account with id: {decode_account_id}")
        
        authorizationFuntions:AuthorizationFuntions = AuthorizationFuntions( db_session=db_session,
                                                                            model_account=account)
    

        try:
            modelRole = authorizationFuntions.get_role_with_name(role_name=role_name)
            if not modelRole:      
                raise Exception()
        except Exception as e:
            raise Exception(f"|$ARL1002 Role {role_name} not found in database")
        
        try:
            modelLevel = authorizationFuntions.get_level_with_name(level_name=level_name)   
            if not modelLevel:      
                raise Exception()
        except Exception as e:
            raise Exception(f"|$ARL1003 Level {level_name} not found in database")
        

        try:
            account_role_level = authorizationFuntions.assign_role_level_to_account(role_id=modelRole.id,
                                                                              level_id=modelLevel.id,
                                                                              )
        except Exception as e:
            db_session.rollback()
            raise Exception(f"|$ARL1004 - Error to assing role and level to account {account_id}  error: {e}")
        db_session.close()
        return AssignRoleLevel(account_role_level=account_role_level)
        
