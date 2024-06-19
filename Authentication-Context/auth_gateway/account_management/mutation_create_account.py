from typing import Dict
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from account_management.account_components import AccountPersonLocation
from account_management.account_attribute import AccountAttribute, LocationAttribute, PersonAttribute
from auth_model_sqlalchemy_14.account_role_level import ModelAccountRoleLevel
from auth_model_sqlalchemy_14.base import db_session
from auth_model_sqlalchemy_14.account import ModelAccount
from auth_model_sqlalchemy_14.level import ModelLevel
from auth_model_sqlalchemy_14.location import ModelLocation
from auth_model_sqlalchemy_14.person import ModelPerson
from auth_model_sqlalchemy_14.role import ModelRole


class Role(SQLAlchemyObjectType):
    class Meta:
        model = ModelRole
        interfaces = (graphene.relay.Node, )


class Level(SQLAlchemyObjectType):
    
    class Meta:
        model = ModelLevel
        interfaces = (graphene.relay.Node, )

class AccountRoleLevel(SQLAlchemyObjectType):
    class Meta:
        model = ModelAccountRoleLevel
        interfaces = (graphene.relay.Node, )



class Person(SQLAlchemyObjectType):
    class Meta:
        model = ModelPerson
        interfaces = (graphene.relay.Node, )
        
class Location(SQLAlchemyObjectType):
    class Meta:
        model = ModelLocation
        interfaces = (graphene.relay.Node, )


class AccountExclude(SQLAlchemyObjectType):
    """AccountExclude node."""

    class Meta:
        model = ModelAccount
        exclude_fields = (
            "password",
        )
        interfaces = (graphene.relay.Node,)

class AccountGraphAttribute:
    user_name = graphene.String(description="User Name of the account max len 30.", required=False)
    password = graphene.String(description="Password of the account.", required=True)
    email = graphene.String(description="Email of the account.", required=True)

class PersonGraphAttribute:
    name = graphene.String(description="Name of the person.", required=True)
    surname = graphene.String(description="Surname of the person.", required=False)
    phone_number = graphene.String(description="Phone number of the person.", required=True)

class LocationGraphAttribute:
    address = graphene.String(description="Address of the location.", required=True)
    city = graphene.String(description="City of the location.", required=True)
    zipcode = graphene.String(description="Zipcode of the location.", required=False)
    map_address = graphene.String(description="Map address of the location.", required=False)

class Account(SQLAlchemyObjectType):
    """Account node."""

    class Meta:
        model = ModelAccount
        interfaces = (graphene.relay.Node,)


class CreateAccountInput(graphene.InputObjectType, AccountGraphAttribute):
    """Arguments to create a account."""
    pass
class CreatePersonInput(graphene.InputObjectType, PersonGraphAttribute):
    """Arguments to create a person."""
    pass

class CreateLocationInput(graphene.InputObjectType, LocationGraphAttribute):
    """Arguments to create a location."""
    pass

class CreateAccount(graphene.Mutation):
    """Mutation to create a account."""

    account = graphene.Field(
        lambda: Account, description="Account node created by this mutation."
    )
   
    token = graphene.String()

    class Arguments:
        account = CreateAccountInput(required=True)
        person = CreatePersonInput(required=True)
        location = CreateLocationInput(required=True)

    
    def mutate(self, info, account:Dict, person:Dict, location:Dict):
        

        account_attr:AccountAttribute = AccountAttribute().from_dict(data=account)
        person_attr = PersonAttribute().from_dict(data=person)
        location_attr = LocationAttribute().from_dict(data=location)        
        componentsAccount = AccountPersonLocation(db_session)

        try:
            modelAccount:ModelAccount = componentsAccount.create_account(account_attr=account_attr,
                                                                  commit_to_db=False)  
        
        except Exception as e:
            db_session.rollback()
            db_session.close()
            raise Exception(
                f"|$AC1001 - Error to create account for {account_attr.user_name}, {e}"
            )
        
        person_attr.account_id = modelAccount.id
        if not person_attr.account_id:
            raise Exception(f"|$AC1002 - Error to create person for {account_attr.user_name} error: account_id is None")
        
        modelPerson = componentsAccount.create_person(person_attr=person_attr,
                                                        commit_to_db=False)
        location_attr.person_id = modelPerson.id
        
        if not location_attr.person_id:
            raise Exception(f"|$AC1003 - Error to create location for {account_attr.user_name} ")
        try:
            componentsAccount.create_location(location_attr=location_attr,
                                                        commit_to_db=False)
        except Exception as e:
            db_session.rollback()
            db_session.close()
            raise Exception(
                f"|$AC1004 - Error to create account for {account_attr.user_name} error: {e.__cause__}"
            )
        try:
            token = componentsAccount.create_access_token(    
               modelAccount.user_name,
               modelAccount.id,
            )
            db_session.commit()
            modelAccount = componentsAccount.get_account_by_id(account_id=modelAccount.id)

        except Exception as e:
            db_session.rollback()
            db_session.close()
            raise Exception(
                f"|$AC1005 - Error to create account for {account_attr.user_name} error: {e.__cause__}"
            )

        return CreateAccount(
            account=modelAccount,
            token=token)
        