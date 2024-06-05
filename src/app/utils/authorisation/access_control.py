"""Aceess Control Decorator Functions"""
from functools import wraps
from flask import request, make_response
from src.main import app_logger
from src.app.database.pbac_queries.permissions import user_permissions
from src.app.utils.authorisation.jwt_token import jwt_auth

def verify_auth(permission_needed):
    def inner_func(main_fuction):
        @wraps(main_fuction)
        def wrapper_func(*args,**kwargs):
            try:
                access_token = request.headers["authorization"].replace("Bearer ", "")
                args_list = list(kwargs.values())
                if args_list:
                    u_id = args_list[0]
                    is_authorised = access_validator(access_token, permission_needed, u_id)
                else:
                    is_authorised = access_validator(access_token, permission_needed)
                if is_authorised:
                    return main_fuction(*args, **kwargs)
                return make_response({"response": "Unauthorised Request"}, 401)
            except ValueError as value_error:
                app_logger.error("token is expired")
                return make_response({"response": str(value_error)}, 401)
            except Exception:
                app_logger.error("Invalid token")
                return make_response({"response": "Unauthorised Request"}, 401)
        return wrapper_func
    return inner_func


def access_validator(access_token, permission_needed, u_id=None):
    user_data = jwt_auth.decode_access_token(access_token)
    if user_data:
        user = user_permissions.verify_user_role(user_data)
        if user:
            permissions = user_permissions.get_permission_list(user_data)
            permission_exists = list(set(permission_needed) & set(permissions))
            if permission_exists:
                if ((permission_exists[0].find("self") == -1) or \
                    (u_id != None and u_id == user_data["user_id"])):
                    return True
    return False
    