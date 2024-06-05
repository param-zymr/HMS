"""Doctor data validator"""
from src.app.utils.validation.data_validation import BaseDataValidation
from src.app.utils.validation.regex_validation import regex_validator

class DataValidation(BaseDataValidation):
    def data_validator_create(self, data) -> bool:
        email = regex_validator.email_validator(data["DOC_EMAIL"])
        password = regex_validator.password_validator(data["DOC_PASSWORD"])
        phone = regex_validator.phone_validator(data["DOC_CELL"])
        altr_phone = regex_validator.phone_validator(data["DOC_ALTR_CELL"])
        licence_number = regex_validator.licence_validator(data["DOC_LICENCE_NUMBER"])
        if False in [email, password, phone, altr_phone, licence_number]:
            return False
        return True
    
    
    def data_validator_update(self, data) -> bool:
        email = regex_validator.email_validator(data["DOC_EMAIL"])
        phone = regex_validator.phone_validator(data["DOC_CELL"])
        altr_phone = regex_validator.phone_validator(data["DOC_ALTR_CELL"])
        licence_number = regex_validator.licence_validator(data["DOC_LICENCE_NUMBER"])
        if False in [email, phone, altr_phone, licence_number]:
            return False
        return True
    
    
    def data_eliminate_password(self, data) -> dict:
        if "DOC_PASSWORD" in data:
            del data["DOC_PASSWORD"]
        if "DOC_PASSWORD_SALT" in data:
            del data["DOC_PASSWORD_SALT"]
        return data

doctor_validator = DataValidation()
