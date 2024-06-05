"""Receptionist data validator"""
from src.app.utils.validation.data_validation import BaseDataValidation
from src.app.utils.validation.regex_validation import regex_validator

class DataValidation(BaseDataValidation):
    def data_validator_create(self, data) -> bool:
        email = regex_validator.email_validator(data["REC_EMAIL"])
        password = regex_validator.password_validator(data["REC_PASSWORD"])
        phone = regex_validator.phone_validator(data["REC_CELL"])
        altr_phone = regex_validator.phone_validator(data["REC_ALTR_CELL"])
        if False in [email, password, phone, altr_phone]:
            return False
        return True
    
    
    def data_validator_update(self, data) -> bool:
        email = regex_validator.email_validator(data["REC_EMAIL"])
        phone = regex_validator.phone_validator(data["REC_CELL"])
        altr_phone = regex_validator.phone_validator(data["REC_ALTR_CELL"])
        if False in [email, phone, altr_phone]:
            return False
        return True
    
    
    def data_eliminate_password(self, data) -> dict:
        if "REC_PASSWORD" in data:
            del data["REC_PASSWORD"]
        if "REC_PASSWORD_SALT" in data:
            del data["REC_PASSWORD_SALT"]
        return data

receptionist_validator = DataValidation()
