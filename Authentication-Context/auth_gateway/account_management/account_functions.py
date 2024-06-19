import os
from account_management.account_attribute import AccountAttribute
from auth_model_sqlalchemy_14.account import ModelAccount
from sqlalchemy.orm import Session
from utils import limit_text, random_varchar_k, remove_symbols_white_to_lower
from datetime import datetime, timedelta
import jwt
import re


class AccountFuntions():
    
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    
    # Warning !
    # If the secret key undergoes a change,
    # it will result in an automatic modification of the password.
    # Consequently, all users will be required to reset their passwords.
    
    def __init__(self, session: Session):
        self.session = session

        if self.session is None:
            raise Exception("AccountFuntions: the session is None")
    
    def get_account_with_user_and_password(self, user_name, password:str) -> bool:
        """ return ModelAccount if user_name and password is correct """
        accountAttribute=AccountAttribute(password=password)
        accountAttribute.check_format_password()
        encode_password:str = accountAttribute.get_encode_password()
        
        try:

            model_account = (
                self.session.query(ModelAccount)
                .filter_by(user_name=user_name, password=encode_password)
                .first()
            )
        except Exception as e:
            raise Exception(f"Error to get account with user_name and password, {e}")       
        
        return model_account

    def get_account_with_email_and_password(self, email, password:str) -> bool:
        """ return ModelAccount if user_name and password is correct """
        accountAttribute=AccountAttribute(password=password)
        accountAttribute.check_format_password()
        encode_password:str = accountAttribute.get_encode_password()
        
        try:

            model_account = (
                self.session.query(ModelAccount)
                .filter_by(email=email, password=encode_password)
                .first()
            )
        except Exception as e:
            raise Exception(f"Error to get account with user_name and password, {e}")       
        
        return model_account
    

        
    def check_available_user_name(self, user_name:str) -> bool:
        """ check if user_name is available """

        count_result = (
            self.session.query(ModelAccount.user_name)
            .filter_by(user_name=user_name)
            .count()
        )
        if count_result == 0:
            return True
        else:
            return False

    def guarantee_available_user_name(self, user_name:str) -> str:
        """
        Ensures that the provided user_name is available by appending a random string if necessary.
        
        Args:
            user_name (str): The user_name to be checked and modified if necessary.
            
        Returns:
            str: The modified user_name that is guaranteed to be available.
            
        Raises:
            Exception: If the maximum number of iterations is reached without finding an available user_name.
        """
        is_available_user_name:bool= self.check_available_user_name(user_name)
        overflow_count:int = 0
        max_iterations_count:int = 100
        
        while is_available_user_name == False:
            overflow_count += 1
            possible = f"{user_name}-{(random_varchar_k(3))}"
            is_available_user_name = self.check_available_user_name(possible)
            if is_available_user_name:
                user_name = possible

            if overflow_count > max_iterations_count:
                raise Exception(
                    "Error to create user_name, overflow_count > 100"
                )
        return user_name


    def create_user_name(self, email:str) -> str:
        """
        Creates a user name based on the given email address.

        Args:
            email (str): The email address of the user.

        Returns:
            str: The generated user name.
        """
        
        def remove_after_at_sign(email_account:str):
            if email_account:
                user_name_raw = email_account.split("@", 1)
                user_name_raw = user_name_raw[0]
                return user_name_raw

        user_name_raw = remove_after_at_sign(email)
        user_name = remove_symbols_white_to_lower(user_name_raw)
        user_name = limit_text(user_name, 16)
        return user_name

    def is_valid_email(self, email:str) -> bool:
        """ check if email is valid """
        if email:
            return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))
        else:
            return False
    
    def check_available_email(self, email:str) -> bool:
        """ check if email is available """

        count_result = (
            self.session.query(ModelAccount.email)
            .filter_by(email=email)
            .count()
        )
        if count_result == 0:
            return True
        else:
            return False
        
        
    def create_access_token(self, username:str, account_id:int, external_id:str=None, is_root:bool=False) -> str:
        
        payload = {
                'username':username,
                'account_id':account_id,
                'external_id':external_id,
                'is_root':is_root,
                'iat':datetime.utcnow(),
                'exp':datetime.utcnow() + timedelta(weeks=20) # TODO: Change to 1 hour in production, I have set it to 20 weeks for develoment time purposes.
            }
        
        token = jwt.encode(
            payload,
            self.JWT_SECRET_KEY,
            algorithm='HS256')
        
        return token
        
    def get_account_by_id(self, account_id:int) -> ModelAccount:
        """
        Retrieves an account from the database based on the provided account ID.

        Args:
            account_id (int): The ID of the account to retrieve.

        Returns:
            ModelAccount: The account object corresponding to the provided account ID.

        Raises:
            Exception: If there is an error while retrieving the account.
        """
        try:
            model_account = (
                self.session.query(ModelAccount)
                .filter_by(id=account_id)
                .first()
            )
        except Exception as e:
            raise Exception(f"Error to get account with account_id, {e}")       
            
        return model_account
    
    def get_account_by_external_id(self, external_id:str) -> ModelAccount:
        """
        Retrieves an account from the database based on the provided external ID.

        Args:
            external_id (str): The external ID of the account to retrieve.

        Returns:
            ModelAccount: The account object corresponding to the provided external ID.

        Raises:
            Exception: If there is an error while retrieving the account.
        """
        try:
            model_account = (
                self.session.query(ModelAccount)
                .filter_by(external_id=external_id)
                .first()
            )
        except Exception as e:
            raise Exception(f"Error to get account with external_id, {e}")       
            
        return model_account
    
    def get_account_by_email(self, email:str) -> ModelAccount:
        """
        Retrieves an account from the database based on the provided email

        Args:
            email (str): 

        Returns:
            ModelAccount: The account object corresponding to the provided email.

        Raises:
            Exception: If there is an error while retrieving the account.
        """
        if email is None:
            raise Exception("Email is required")
        
        if not self.is_valid_email(email):
            raise Exception("Email is not valid") 
        try:
            model_account = (
                self.session.query(ModelAccount)
                .filter_by(email=email)
                .first()
            )
        except Exception as e:
            raise Exception(f"Error to get account with external_id, {e}")       
            
        return model_account
    
    