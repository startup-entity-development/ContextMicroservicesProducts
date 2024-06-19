""" This module contains the authorization middleware."""
from functools import wraps
from flask import request
import requests as http_request
from settings import USER_AUTH_ROOT
from exceptions import (
    MisusedDecoratorException,
    InternalServerException,
    ForbiddenException,
)


def require_permission_external(
    root_user: bool = False,
    role_name: str = None,
    level_name: str = None,
) -> None:
    """Authorization decorator for external services

    Args:
        root_user (bool, optional): If True, the user is required to be root.
        role_name (str, optional): The required role name.
        level_name (str, optional): The required level name.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            account_id = request.headers.get("X-Auth-Id")
            account_name = request.headers.get("X-Auth-User")
            if not root_user and not role_name and not level_name:
                raise MisusedDecoratorException(
                    message="""Detected misuse of the decorator
                    "require_permission_external".
                    required role_name and level_name or root_user=True"""
                )

            if not account_id and not account_name:
                return {"message": "Forbidden, account_id not found"}, 403

            if not account_id and account_name == USER_AUTH_ROOT and root_user:
                return func(*args, **kwargs)

            try:
                account_id: int = int(account_id)

                resp = http_request.get(
                    "http://172.17.0.1:8881/public/auth/permissions",
                    {"account_id": account_id},
                    timeout=10,
                )
                _resp = resp.json()
                permissions = _resp.get("data", [])

                for permission in permissions:
                    if permission.get("role_name") == role_name and (
                        permission.get("level_name") == level_name
                        or permission.get("level_value") > __get_level_value(level_name)
                    ):
                        return func(*args, **kwargs)

            except InternalServerException as e:
                return {
                    "message": f"Internal Server Error {e}",
                    "error_code": 107,
                }, 500

            raise ForbiddenException(
                f"""Forbidden, is required permission with role_name:
                {role_name} and level_name: {level_name}"""
            )

        return wrapper

    return decorator


def __get_level_value(level_name: str) -> int:
    """Get the level value from the level name"""
    # TODO:Add correct functiong to get this from database
    level_value = 0
    if level_name == "level_1":
        level_value = 1
    elif level_name == "level_2":
        level_value = 2
    elif level_name == "level_3":
        level_value = 3
    return level_value
