
import graphene
from account_management.account_functions import AccountFuntions
from account_management.mutation_create_account import AccountExclude
from auth_model_sqlalchemy_14.account import ModelAccount
from auth_model_sqlalchemy_14.base import db_session


class LoginAccount(graphene.Mutation):
    
    account = graphene.Field(lambda: AccountExclude, description="Role node created by this mutation.")
    token = graphene.String(description="Token to access to the API", required=True)

    class Arguments:
        
        user=graphene.String(description="User name or Email of the account", required=True)
        password = graphene.String(description="Level Name", required=True)

    def mutate(self, info, user, password):
        accountFuntions:AccountFuntions =  AccountFuntions(session=db_session)
        is_email:bool= accountFuntions.is_valid_email(email=user)
        token:str = ""
        account:ModelAccount = None
        if is_email:
            account:ModelAccount = accountFuntions.get_account_with_email_and_password(email=user,
                                                                                password=password)
            if not account:
                raise Exception("$|LA1000 Email or password incorrect'")
        else:
            account:ModelAccount = accountFuntions.get_account_with_user_and_password(user_name=user,
                                                                                    password=password)       
            if not account:
                raise Exception("$|LA1001 User name or password incorrect'")
    
        if account.is_soft_deleted:
            raise Exception("|LA1002 Account is deleted")
            
        token = accountFuntions.create_access_token(
            username=account.user_name,
            account_id=account.id)   
        
        return LoginAccount(account=account, token=token)
    


