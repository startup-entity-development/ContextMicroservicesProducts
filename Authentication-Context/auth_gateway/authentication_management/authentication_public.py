import os
import traceback
from typing import  Tuple
from flask import Blueprint, request
from account_management.account_attribute import AccountAttribute
from account_management.account_functions import AccountFuntions
from auth_model_sqlalchemy_14.account import ModelAccount
from auth_model_sqlalchemy_14.base import db_session
api = Blueprint('public_api', __name__)

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

""" 
 Warning !
 If the JWT_SECRET_KEY undergoes a change,
 it will result in an automatic modification of the password.
 Consequently, all users will be required to reset their passwords.

 """

USER_AUTH_ROOT = os.environ.get('USER_AUTH_ROOT')
USER_AUTH_PASSWORD_MD5 = os.environ.get('USER_AUTH_PASSWORD_MD5')


def check_login_arguments(request) -> Tuple[str, str]:
    try:
        username = request.form['username']
    except KeyError:
        return  {'message':'Bad Request, User name is required', 'error_code':101}, 400
    try:
        password = request.form['password']
    except KeyError:
        return  {'message':'Bad Request, User password is required','error_code':102}, 400
    
    return username, password


@api.get('/login_auth_root')
def login_auth_root():
    """
    Authenticates the login credentials for the root user.
    
    Returns:
        dict: A dictionary containing the token and message if the authentication is successful.
              Otherwise, returns a dictionary with an error message and error code.
    ghp!123
    """
    username, password = check_login_arguments(request)
    if username == USER_AUTH_ROOT:
        account_attr = AccountAttribute(password=password)
        account_attr.check_format_password()
        encode_password:str = account_attr.get_encode_password()
        if encode_password != USER_AUTH_PASSWORD_MD5:
            return {'message':'User authentication root password incorrect', 'error_code':103}, 401
        
        accountFuntions:AccountFuntions =  AccountFuntions(session=db_session)
        token = accountFuntions.create_access_token(
            username=username,
            account_id=None,
            is_root=True)
        
        return {
            'token':token,
            'message':'Authorization: Bearer xxx'
        }, 200
    else:
        return {'message':'User name incorrect', 'error_code':104}, 401

@api.post('/login')
def login():
    username, password = check_login_arguments(request)
    try:
        accountFuntions:AccountFuntions =  AccountFuntions(session=db_session)
        account:ModelAccount = accountFuntions.get_account_with_user_and_password(user_name=username,
                                                                                password=password)       

        if not account:
            return { 'message': 'User name or password incorrect', 'error_code':105 }, 401
        if account.is_soft_deleted:
            return { 'message': 'Account is deleted', 'error_code':106 }, 401
        
        token = accountFuntions.create_access_token(
            username=username,
            account_id=account.id)
        
        return {
            'token':token,
            'message':'Authorization: Bearer xxx'
        }, 200
    except:
        traceback.print_exc()
        return { 'message' : 'Internal Server Error'}, 500
        

@api.post('/logout')
def logout():
    # Implement token revocation
    ...
    return {
        'message':'Success'
    }, 200




