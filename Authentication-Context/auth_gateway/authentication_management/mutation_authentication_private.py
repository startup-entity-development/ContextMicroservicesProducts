import os
from flask import request
import graphene
from account_management.account_components import AccountPersonLocation
from auth_model_sqlalchemy_14.base import db_session

USER_AUTH_ROOT = os.environ.get('USER_AUTH_ROOT')

class ProtectedSoftDeleteAccount(graphene.Mutation):
    
    message = graphene.String(description="Message result", required=True)

    class Arguments:
        reason=graphene.String(description="Reson why the account is deleted", required=False)
        
    def mutate(self, info, reason:str):
        account_id = request.headers.get('X-Auth-Id')
        account_name = request.headers.get('X-Auth-User')
        
        if account_name == USER_AUTH_ROOT:
            raise Exception('Is not possible soft delete root user : {}'.format(account_name))
        
        account_id = int(account_id)   
        accountPersonLocation = AccountPersonLocation(session=db_session)
        accountPersonLocation.soft_delete_account(reason=reason, account_id=account_id)

        return ProtectedSoftDeleteAccount(message=f"Account {account_name} is soft deleted")
    