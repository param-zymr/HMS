"""Patient data validator"""
from src.app.utils.validation.data_validation import BaseDataValidation
from src.app.utils.validation.regex_validation import regex_validator

class DataValidation(BaseDataValidation):
    def data_validator_create(self, data) -> bool:
        email = regex_validator.email_validator(data["PAT_EMAIL"])
        password = regex_validator.password_validator(data["PAT_PASSWORD"])
        phone = regex_validator.phone_validator(data["PAT_CELL"])
        altr_phone = regex_validator.phone_validator(data["PAT_ALTR_CELL"])
        family_doc_phone = regex_validator.phone_validator(data["PAT_FAMILY_DOC_CELL"])
        adhar = regex_validator.aadhaar_validator(data["PAT_ADHAR"])
        zip_code = regex_validator.zipcode_validator(data["PAT_ZIP"])
        if False in [email, password, phone, altr_phone, family_doc_phone, adhar, zip_code]:
            return False
        return True
    
    
    def data_validator_update(self, data) -> bool:
        email = regex_validator.email_validator(data["PAT_EMAIL"])
        phone = regex_validator.phone_validator(data["PAT_CELL"])
        altr_phone = regex_validator.phone_validator(data["PAT_ALTR_CELL"])
        family_doc_phone = regex_validator.phone_validator(data["PAT_FAMILY_DOC_CELL"])
        adhar = regex_validator.aadhaar_validator(data["PAT_ADHAR"])
        zip_code = regex_validator.zipcode_validator(data["PAT_ZIP"])
        if False in [email, phone, altr_phone, family_doc_phone, adhar, zip_code]:
            return False
        return True
    
    
    def data_eliminate_password(self, data) -> dict:
        if "PAT_PASSWORD" in data:
            del data["PAT_PASSWORD"]
        if "PAT_PASSWORD_SALT" in data:
            del data["PAT_PASSWORD_SALT"]
        return data

patient_validator = DataValidation()
