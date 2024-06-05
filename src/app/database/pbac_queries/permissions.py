"""User Permissions Database Queries"""
from sqlalchemy import text
from psycopg2.extensions import AsIs
from src.app.models.user_catagories import UserCatagories
from src.app.models.roles import Roles
from src.app.models.permissions import Permissions
from src.app.models.ucat_roles_mapper import UcatRoles
from src.app.models.role_permissions_mapper import RolePermissions
from src.app.models.ucat_permissions_mapper import UcatPermissions
from src.main import app_logger, db
from src.app.config import app_settings
from src.app.utils.security.encryption import hashing

class UserPermissions:
    def get_permission_list(self, user_data):
        user_permissions, role_permissions, applicable_permissions = ([] for i in range(3))
        user_permissions_result = UserCatagories.query\
            .join(UcatPermissions, UserCatagories.UCAT_UNIQ_ID == UcatPermissions.UCAT_ID)\
            .join(Permissions, UcatPermissions.PAR_ID == Permissions.PAR_UNIQ_ID)\
            .filter(UserCatagories.USER_CATAGORY == user_data["user_catagory"]).all()
        role_permissions_result = Roles.query\
            .join(RolePermissions, Roles.ROLE_UNIQ_ID == RolePermissions.ROLE_ID)\
            .join(Permissions, RolePermissions.PAR_ID == Permissions.PAR_UNIQ_ID)\
            .filter(Roles.ROLE == user_data["user_role"]).all()
        if user_permissions_result[0].UCAT_PERMISSIONS:
            for row in user_permissions_result[0].UCAT_PERMISSIONS:
                user_permissions.append(row.permissions.PERMISSION)
        if role_permissions_result[0].ROLE_PERMISSIONS:
            for row in role_permissions_result[0].ROLE_PERMISSIONS:
                role_permissions.append(row.permissions.PERMISSION)
        applicable_permissions = list(set(user_permissions) & set(role_permissions))
        app_logger.info("user permissions list fetched from db")
        return applicable_permissions
    
    
    def get_user(self, user_data):
        user_table_name = user_data["USER_CATAGORY"] + "_details"
        user_catagory_prefix = app_settings.USER_CATAGORY_PREFIX[user_data["USER_CATAGORY"]]
        email_column = user_catagory_prefix + "_EMAIL"
        sql = text('SELECT * FROM :user_table_name WHERE \
            ":email_column" = '"':user_email'"'')
        sql_params = {"user_table_name":AsIs(user_table_name), \
            "email_column":AsIs(email_column), "user_email":AsIs(user_data["EMAIL"])}
        result = db.session.execute(sql, sql_params).mappings().all()
        if result:
            result_data = result[0]
            if hashing.verify_password(user_data["PASSWORD"], \
                result_data[user_catagory_prefix+"_PASSWORD"], \
                result_data[user_catagory_prefix+"_PASSWORD_SALT"]):
                return result_data
        return
    
    
    def verify_user_role(self, user_data):
        user_table_name = user_data["user_catagory"] + "_details"
        id_column = app_settings.USER_CATAGORY_PREFIX[user_data["user_catagory"]]\
            + "_UNIQ_ID"
        role_column = app_settings.USER_CATAGORY_PREFIX[user_data["user_catagory"]]\
            + "_ROLE"
        sql = text('SELECT * FROM :user_table_name WHERE ":id_column" = '":user_id"' \
            AND ":role_column" = '"':user_role'"'')
        sql_params = {"user_table_name":AsIs(user_table_name), "id_column":AsIs(id_column),\
            "user_id":AsIs(user_data["user_id"]), "role_column":AsIs(role_column), \
            "user_role":AsIs(user_data["user_role"])}
        result = db.session.execute(sql, sql_params).mappings().all()
        return result
    
    
user_permissions = UserPermissions()
