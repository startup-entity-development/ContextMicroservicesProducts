
from typing import Dict
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from auth_model_sqlalchemy_14.account_role_level import ModelAccountRoleLevel
from auth_model_sqlalchemy_14.level import ModelLevel
from auth_model_sqlalchemy_14.role import ModelRole
from authorization_management.authorization_components import AuthorizationComponents
from authorization_management.role_level_dataclass import RoleAttribute, LevelAttribute
from auth_model_sqlalchemy_14.base import db_session
from authorization_management.authorization_middleware import require_permission_internal

class Role(SQLAlchemyObjectType):
    class Meta:
        model = ModelRole
        interfaces = (graphene.relay.Node, )


class Level(SQLAlchemyObjectType):
    class Meta:
        model = ModelLevel
        interfaces = (graphene.relay.Node, )


class RoleLevel(SQLAlchemyObjectType):
    class Meta:
        model = ModelAccountRoleLevel
        interfaces = (graphene.relay.Node, )


class RoleGraphAttribute:
    role_name = graphene.String(description="Role Name", required=True)
    definition = graphene.String(description="Definition of the Role", required=True)


class LevelGraphAttribute:
    level_name = graphene.String(description="Level Name", required=True)
    level_value = graphene.Int(description="Level Value", required=True)
    definition = graphene.String(description="Definition of the Level", required=True)


class CreateRoleInput(graphene.InputObjectType, RoleGraphAttribute):
    """Arguments to create a role."""
    pass


class CreateLevelInput(graphene.InputObjectType, LevelGraphAttribute):
    """Arguments to create a level."""
    pass


class CreateRole(graphene.Mutation):
    """Mutation to create a role."""

    role = graphene.Field(lambda: Role, description="Role node created by this mutation.")
   
    class Arguments:
        input = CreateRoleInput(required=True)
    
    @require_permission_internal(root_user= True, role_name='root', level_name='level_1')
    def mutate(self, info, input:Dict):
        

        role_attr = RoleAttribute().from_dict(data=input)
        auth_components = AuthorizationComponents(db_session)
        try:
            model_role :ModelRole = auth_components.create_role(role_attr=role_attr,
                                                                            commit_to_db=True)  
        
        except Exception as e:

            raise Exception(
                f"|$CR101 - Error to create role for {role_attr.role_name}, {e}"
            )
        
        finally:
            db_session.close()

        return CreateRole(role=model_role,)
    

class CreateLevel(graphene.Mutation):
    """Mutation to create a level."""

    level = graphene.Field(
        lambda: Level, description="Level node created by this mutation."
    )
   

    class Arguments:
        input = CreateLevelInput(required=True)
    
    @require_permission_internal(root_user= True)
    def mutate(self, info, input:Dict):
        

        level_attr = LevelAttribute().from_dict(data=input)
        auth_components = AuthorizationComponents(db_session)
        try:
            model_level :ModelLevel = auth_components.create_level(level_attr=level_attr,
                                                                            commit_to_db=True)  
        
        except Exception as e:

            raise Exception(
                f"|$CL101 - Error to create level for {level_attr.level_name}"
            )
        
        finally:
            db_session.close()
        
        return CreateLevel(level=model_level,)
        