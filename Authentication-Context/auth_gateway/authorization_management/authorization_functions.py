from typing import List
from account_management.mutation_create_account import AccountExclude
from auth_model_sqlalchemy_14.account import ModelAccount
from auth_model_sqlalchemy_14.account_role_level import ModelAccountRoleLevel
from auth_model_sqlalchemy_14.level import ModelLevel
from auth_model_sqlalchemy_14.role import ModelRole
from authorization_management.role_level_dataclass import RoleAttribute, LevelAttribute


class AuthorizationFuntions():

    def __init__(self,db_session ,model_account:ModelAccount):
        self.account:ModelAccount =  model_account
        self.db_session = db_session

        
    def get_account_role_level_list(self) -> List[ModelAccountRoleLevel]|None:
        
        try:
            list_modelAccountRole:ModelAccountRoleLevel = self.db_session.query(ModelAccountRoleLevel).filter_by(account_id=self.account.id)
        except Exception as e:
            return None
        return list_modelAccountRole

    def assign_role_level_to_account(self, role_id:int, level_id: int, auto_commit:bool=True) -> ModelAccountRoleLevel:
        
        if not self.account:
            raise Exception("Account is Required")
        level_of_account_role:str = self.check_if_account_has_role_level(role_id=role_id)
        if level_of_account_role:
            raise Exception(f"Account already has this role with a level: {level_of_account_role},if yo want to change the level, please use the update function")
            
        account_role_level = ModelAccountRoleLevel(
            account_id=self.account.id,
            role_id=role_id,
            is_active=True,
            level_id=level_id)
        
        self.db_session.add(account_role_level)
        if auto_commit:
            self.db_session.commit()
        else:
            self.db_session.flush()
        self.db_session.refresh(account_role_level)
        return account_role_level
    
    def check_if_account_has_role_level(self, role_id:int) -> str|None:
        account_role_level:ModelAccountRoleLevel = self.db_session.query(ModelAccountRoleLevel).filter_by(account_id=self.account.id, role_id=role_id).first()
        if account_role_level:
            return account_role_level.level.level_name
        return None
    
    def get_role_with_name(self, role_name:str) -> ModelRole:
        model_role:ModelRole = self.db_session.query(ModelRole).filter_by(role_name=role_name).first()
        return model_role
    
    def get_level_with_name(self, level_name:str) -> ModelLevel:
        model_level:ModelLevel = self.db_session.query(ModelLevel).filter_by(level_name=level_name).first()
        return model_level
    

        
    
