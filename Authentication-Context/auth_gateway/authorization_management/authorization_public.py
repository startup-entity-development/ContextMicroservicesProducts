import os
import traceback
from typing import  Dict, Tuple
from flask import Blueprint, request
import jwt
from account_management.account_functions import AccountFuntions
from auth_model_sqlalchemy_14.account import ModelAccount
from auth_model_sqlalchemy_14.base import db_session
from authorization_management.authorization_functions import AuthorizationFuntions
api = Blueprint('public_api_authorization', __name__)

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')



@api.get('/permissions')
def get_permissions():
    account_id = request.args.get('account_id')
    account_id = int(account_id)
    return permissions_account(account_id=account_id)
   

def permissions_account(account_id:int) -> Tuple[Dict[str, str], int]:
    
    account_funcionts = AccountFuntions(session=db_session)
    account:ModelAccount  = account_funcionts.get_account_by_id(account_id=account_id)
    
    if not account:
        return {
            'message':'Account Not Found',
            'data':[]
        }, 400
    
    if account.is_soft_deleted:
        return {
            'message':'Account is deleted',
            'data':[]
        }, 400
    
    authorization_management = AuthorizationFuntions(db_session=db_session,
                                                      model_account=account)
    
    if not account.id:
        return {
            'message':'Account Not Found',
            'data':[]
        }, 400
    
    list_account_role_level = authorization_management.get_account_role_level_list()

  
   
    if not list_account_role_level:
        return {
            'message':'Account without permissions',
            'data':[]
        }, 400
    
    authorization_role_level = {}
    list_permissions = []

    for account_role_level in list_account_role_level: 
       authorization_role_level["role_name"] = account_role_level.role.role_name
       authorization_role_level["level_name"] = account_role_level.level.level_name
       authorization_role_level["level_value"] = account_role_level.level.level_value
       list_permissions.append(authorization_role_level)
    db_session.close()
    return {
        'data':list_permissions,
        'message':'OK'
    }, 200
    
@api.get('/token/info')
def get_token_info():

    jwt_access_token = request.args.get('access_token')
    if not jwt_access_token:
        return { 'message': 'Bad Request'}, 400
    

    try:
        payload = jwt.decode(
            jwt_access_token,
            JWT_SECRET_KEY,
            algorithms = ['HS256'],
            verify = True)

        if not payload.get('is_root', False) :
            account_id = payload.get('account_id')
            account_id = int(account_id)
            account_funcionts = AccountFuntions(session=db_session)
            account:ModelAccount  = account_funcionts.get_account_by_id(account_id=account_id)
            if not account:
                return { 'message': 'Bad Request Account Not Found','error_code':101}, 500
            if account.is_soft_deleted:
                return { 'message': 'Bad Request Account is deleted','error_code':102}, 500
    
        return { 'message': 'OK', 'data': payload }, 200
    except jwt.exceptions.ExpiredSignatureError:
        return { 'message': 'Bad Request ExpiredSignatureError ','error_code':104}, 500
    except jwt.exceptions.InvalidTokenError:
        return { 'message': 'Bad Request InvalidTokenError ','error_code':105}, 500
    except:
        traceback.print_exc()
        return { 'message' : 'Internal Server Error','error_code':106},500
    finally:
        db_session.close()

if __name__ == '__main__':
    # test get_permissions
    print(permissions_account(account_id=6))