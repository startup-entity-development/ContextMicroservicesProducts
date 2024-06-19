from account_management.account_attribute import AccountAttribute, LocationAttribute, PersonAttribute
from account_management.account_functions import AccountFuntions
from exceptions import AccountManagementException
from auth_model_sqlalchemy_14.account import ModelAccount
from auth_model_sqlalchemy_14.location import ModelLocation
from auth_model_sqlalchemy_14.person import ModelPerson
from sqlalchemy.orm import Session
from utils import limit_text, remove_symbols_white_to_lower


class AccountPersonLocation(AccountFuntions):

    def __init__(self, session: Session):
        self.session = session
        

        if self.session is None:
            raise Exception("the session is None")

    def create_account(self, account_attr: AccountAttribute, commit_to_db:bool=False) -> ModelAccount:
        """ create account """
        if account_attr is None:
            raise AccountManagementException(class_name="AccountPersonLocation",
                                            function_name="create_account",
                                            message="AccountAttribute is required, $CA101",
                                            data_dict=account_attr.to_dict(),
                                                     )

        if not self.is_valid_email(account_attr.email):
            raise AccountManagementException(class_name="AccountPersonLocation",
                                            function_name="create_account",
                                            message="Email is not valid, $CA102",
                                            data_dict=account_attr.to_dict(),
                                                        )
        
        
        if account_attr.user_name is None:
            account_attr.user_name = self.create_user_name(account_attr.email)
        else:
            account_attr.user_name = limit_text(account_attr.user_name, 10)
            account_attr.user_name = remove_symbols_white_to_lower(account_attr.user_name)
        
        account_attr.user_name = self.guarantee_available_user_name(account_attr.user_name) 
        account_attr.external_id = f"account-{account_attr.user_name}"
        try:
            model_account = ModelAccount(**account_attr.to_dict())
            self.session.add(model_account)
            if commit_to_db:
                self.session.commit()
            else:
                self.session.flush()
            self.session.refresh(model_account)
            return model_account
        except Exception as e:
            self.session.rollback()
            if "UniqueViolation" in str(e):
                if "Account_user_name_key" in str(e):
                    raise AccountManagementException(class_name="AccountPersonLocation",
                                                    function_name="create_account",
                                                     message="User_name is already registered, $CA103",
                                                     data_dict=account_attr.to_dict(),
                                                     )
                if "Account_email_key" in str(e):
                    raise AccountManagementException(class_name="AccountPersonLocation",
                                                    function_name="create_account",
                                                     message="Email is already registered, $CA104",
                                                     data_dict=account_attr.to_dict(),

                                                     )
                
                raise Exception(f"UniqueViolation, method create_account {e}, $CA105 ")
            
            raise Exception(f"AccountPersonLocation, method create_account {e}, $CA106 ")   
        

    def soft_delete_account(self, account_id: int, reason: str) -> ModelAccount:
        """ will soft delete account """
        try:
            model_account:ModelAccount = self.session.query(ModelAccount).filter(ModelAccount.id == account_id).first()
            if model_account is None:
                raise Exception(f"AccountPersonLocation, method soft_delete_account, model_account is None, $SDA101")
            if model_account.is_soft_deleted:
                raise Exception(f"AccountPersonLocation, method soft_delete_account, model_account is already soft deleted, $SDA102")
            model_account.is_soft_deleted = True
            model_account.delete_reason = reason
            self.session.add(model_account)
            self.session.commit()
            self.session.refresh(model_account)
            return model_account
        except Exception as e:
            self.session.close()
            raise Exception(f"AccountPersonLocation, method soft_delete_account {e}, $SDA103")
        
    
    def create_person(self, person_attr: PersonAttribute, commit_to_db:bool=False) -> ModelPerson:
        """ create person """
        try:
            
            if person_attr is None:
                raise Exception("PersonAttribute is required")

            print(person_attr.to_dict())
            model_person = ModelPerson(**person_attr.to_dict())
            self.session.add(model_person)
            self.session.flush()
            self.session.refresh(model_person)

            return model_person
        
        except Exception as e:
            self.session.rollback()
            if  "UniqueViolation" in str(e):
                    raise AccountManagementException(class_name="AccountPersonLocation",
                                                    function_name="create_person",
                                                     message="Phone_number is already registered, $CP101",
                                                     data_dict=person_attr.to_dict(),
                                                     )
            
            raise AccountManagementException(class_name="AccountPersonLocation",
                                            function_name="create_person",
                                            message="Error to create person, $CP102 exception: {e}",
                                            data_dict=person_attr.to_dict(),
                                                     )


    
    def create_location(self, location_attr: LocationAttribute, commit_to_db:bool=False) -> ModelLocation:
        """ create location """
        
        try:
                
            if location_attr is None:
                raise Exception("LocationAttribute is required")
            print(location_attr.to_dict())
            model_location = ModelLocation(**location_attr.to_dict())

            self.session.add(model_location)
            
            if commit_to_db:
                self.session.commit()
            else:
                self.session.flush()
                self.session.refresh(model_location)



            return model_location
        
        except Exception as e:
            self.session.rollback()
            raise AccountManagementException(class_name="AccountPersonLocation",
                                            function_name="create_location",
                                            message="Error to create person, $CP102 exception: {e}",
                                            data_dict=location_attr.to_dict(),
                                                     )
        
 
    


