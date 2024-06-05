"""JWT Access and Refresh Token Generation and Verification"""
from datetime import datetime, timedelta
import jwt
from src.app.config import app_settings

class JWTAuth:
    def generate_access_token(self, user_data):
        payload = {"user_id": user_data["user_id"],
                    "user_catagory": user_data["user_catagory"],
                    "user_role": user_data["user_role"],
                    "time_expires": (datetime.now() + \
                       timedelta(minutes=app_settings.JWT_ACCESS_TOKEN_EXPIRE_TIME)).timestamp()}
        encoded_jwt = jwt.encode(payload, app_settings.JWT_ACCESS_TOKEN_SECRET_KEY, \
            algorithm=app_settings.JWT_ALGORITHM)
        return encoded_jwt
    
    
    def generate_refresh_token(self, user_data):
        payload = {"user_id": user_data["user_id"],
                    "user_catagory": user_data["user_catagory"],
                    "user_role": user_data["user_role"],
                    "time_expires": (datetime.now() + \
                       timedelta(days=app_settings.JWT_REFRESH_TOKEN_EXPIRE_TIME)).timestamp(),
                    "timeout": (datetime.now() + \
                       timedelta(days=app_settings.JWT_REFRESH_TOKEN_TIMEOUT)).timestamp()}
        encoded_jwt = jwt.encode(payload, app_settings.JWT_REFRESH_TOKEN_SECRET_KEY, \
            algorithm=app_settings.JWT_ALGORITHM)
        return encoded_jwt
    
    
    def update_refresh_token(self, user_data):
        payload = {"user_id": user_data["user_id"],
                    "user_catagory": user_data["user_catagory"],
                    "user_role": user_data["user_role"],
                    "time_expires": (datetime.now() + \
                       timedelta(days=app_settings.JWT_REFRESH_TOKEN_EXPIRE_TIME)).timestamp(),
                    "timeout": user_data["timeout"]}
        encoded_jwt = jwt.encode(payload, app_settings.JWT_REFRESH_TOKEN_SECRET_KEY, \
            algorithm=app_settings.JWT_ALGORITHM)
        return encoded_jwt
    
    
    def decode_access_token(self, token):
        payload = jwt.decode(token, app_settings.JWT_ACCESS_TOKEN_SECRET_KEY, \
            algorithms=[app_settings.JWT_ALGORITHM])
        exp_time = datetime.fromtimestamp(payload["time_expires"])
        if exp_time - datetime.now() > timedelta(seconds=1):
            return payload
        raise ValueError("Access token is expired")
    
    
    def decode_refresh_token(self, token):
        payload = jwt.decode(token, app_settings.JWT_REFRESH_TOKEN_SECRET_KEY, \
            algorithms=[app_settings.JWT_ALGORITHM])
        exp_time = datetime.fromtimestamp(payload["time_expires"])
        timeout = datetime.fromtimestamp(payload["timeout"])
        if (timeout - datetime.now() > timedelta(seconds=1)) and \
            (exp_time - datetime.now() > timedelta(seconds=1)):
            return payload
        return
    

jwt_auth = JWTAuth()
