""" This module contains the response type"""
from graphene import ObjectType, String


class Response(ObjectType):
    """Response type"""

    message = String()
