from sqlalchemy.orm import Session
from auth_model_sqlalchemy_14.level import ModelLevel
from auth_model_sqlalchemy_14.role import ModelRole
from exceptions import AuthorizationManagementException
from .role_level_dataclass import RoleAttribute, LevelAttribute

class AuthorizationComponents:

    def __init__(self, session: Session):
        self.session = session

        if self.session is None:
            raise Exception("the session is None")

    def create_role(self, role_attr: RoleAttribute, commit_to_db:bool=False) -> ModelRole:
        """ create role """
        if role_attr is None:
            raise AuthorizationManagementException(class_name="AuthorizationComponents",
                                            function_name="create_role",
                                            message="RoleAttribute is required, $CR101",
                                            data_dict=role_attr.to_dict(),)
        try:
            model_role = ModelRole(**role_attr.to_dict())
            self.session.add(model_role)
            if commit_to_db:
                self.session.commit()
            else:
                self.session.flush()
                self.session.refresh(model_role)
            return model_role
        except Exception as e:
            self.session.close()
            if "UniqueViolation" in str(e):
                if "Role_role_name_key" in str(e):
                    raise AuthorizationManagementException(class_name="AuthorizationComponents",
                                                    function_name="create_role",
                                                     message="role name is already registered, $CR102",
                                                     data_dict=role_attr.to_dict(),
                                                     )
                                
                raise AuthorizationManagementException(class_name="AuthorizationComponents",
                                                       function_name="create_role",
                                                     message=f"UniqueViolation, exception:{e} $CR103",
                                                     data_dict=role_attr.to_dict(),
                                                     )
            
            raise AuthorizationManagementException(class_name="AuthorizationComponents",
                                                       function_name="create_role",
                                                     message=f"Exception:{e} $CR104",
                                                     data_dict=role_attr.to_dict(),
                                                     )   
        
    def create_level(self, level_attr: LevelAttribute, commit_to_db:bool=False) -> ModelLevel:

        """ create level """
        if level_attr is None:
            raise AuthorizationManagementException(class_name="AuthorizationComponents",
                                            function_name="create_level",
                                            message="LevelAttribute is required, $CL101",
                                            data_dict=level_attr.to_dict(),
                                                     )
        try:
            model_level = ModelLevel(**level_attr.to_dict())
            self.session.add(model_level)
            if commit_to_db:
                self.session.commit()
            else:
                self.session.flush()
                self.session.refresh(model_level)
            return model_level
        except Exception as e:
            self.session.close()
            if "UniqueViolation" in str(e):
                if "Level_level_name_key" in str(e):
                    raise AuthorizationManagementException(class_name="AuthorizationComponents",
                                                    function_name="create_level",
                                                     message="level name is already registered, $CL102",
                                                     data_dict=level_attr.to_dict(),
                                                     )
                                
                raise AuthorizationManagementException(class_name="AuthorizationComponents",
                                                       function_name="create_level",
                                                     message=f"UniqueViolation, exception:{e} $CL103",
                                                     data_dict=level_attr.to_dict(),
                                                     )
            
            raise AuthorizationManagementException(class_name="AuthorizationComponents",
                                                       function_name="create_level",
                                                     message=f"Exception:{e} $CL104",
                                                     data_dict=level_attr.to_dict(),
                                                     )
