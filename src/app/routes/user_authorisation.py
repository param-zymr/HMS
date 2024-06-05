"""App User Authorisation Router"""
from flask import Blueprint, request, make_response
from src.main import app_logger, app_settings
from src.app.database.pbac_queries.permissions import user_permissions
from src.app.utils.authorisation.access_control import jwt_auth

user_authorisation = Blueprint('user_authorisation', __name__)

@user_authorisation.route("/get-access-token", methods=["GET"])
def get_aceess_token():
    data = request.json
    user_data = {}
    user_prefix = app_settings.USER_CATAGORY_PREFIX[data["USER_CATAGORY"]]
    user = user_permissions.get_user(data)
    if user:
        user_data["user_id"] = user[user_prefix+"_UNIQ_ID"]
        user_data["user_catagory"] = data["USER_CATAGORY"]
        user_data["user_role"] = user[user_prefix+"_ROLE"]
        app_logger.info("access and refresh token generated")
        return {"access_token":jwt_auth.generate_access_token(user_data),\
            "refresh_token":jwt_auth.generate_refresh_token(user_data)}
    app_logger.warning("no user found")
    return make_response({"Message":"The user does not exists"}, 400)


@user_authorisation.route("/refresh-access-token", methods=["GET"])
def refresh_aceess_token():
    data = request.json
    user_data = jwt_auth.decode_refresh_token(data["REFRESH_TOKEN"])
    if user_data:
        app_logger.info("access and refresh token updated")
        return {"access_token":jwt_auth.generate_access_token(user_data),\
            "refresh_token":jwt_auth.update_refresh_token(user_data)}
    app_logger.warning("invalid refresh token")
    return make_response({"Message":"The refresh token is not valid"}, 400)
