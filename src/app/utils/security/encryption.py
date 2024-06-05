"""General Encryption Functionality"""
import bcrypt
from src.main import app_settings

class Hashing:
    def create_password(self, plain_password, salt) -> str:
        pepper = app_settings.PASSWORD_PEPPER
        password_temp = plain_password + "." + pepper
        password  = password_temp.encode()
        salt_temp = salt.encode()
        hashed_password_temp = bcrypt.hashpw(password, salt_temp)
        hashed_password = hashed_password_temp.decode()
        return hashed_password
    
    
    def verify_password(self, plain_password, db_password, db_salt) -> bool:
        hashed_password = self.create_password(plain_password, db_salt)
        if hashed_password == db_password:
            return True
        return False
    
    
    def create_salt(self) -> str:
        salt_temp = bcrypt.gensalt()
        salt = salt_temp.decode()
        return salt
    
    
hashing = Hashing()
