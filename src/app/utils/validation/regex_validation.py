"""Genaral Regex Validator"""
import re

EMAIL_REGEX = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
PASSWORD_REGEX = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!#%*?&])[A-Za-z\d@#$!%*?&]{8,18}$" \
    # Minimum 8 and maximum 18 characters, at least 1 uppercase letter, \
    # 1 lowercase letter, 1 number and one special character
PHONE_REGEX = "^\+?[0-9]{0,2}[0-9]{10}$"
AADHAAR_REGEX = "^[0-9]{12}$"
LICENCE_NUMBER_REGEX = "^[A-Z0-9]{10}$"
ZIP_CODE_REGEX = "^[0-9]{5,6}$"

class RegexValidator:
    def email_validator(self, email) -> bool:
        if re.fullmatch(EMAIL_REGEX, email):
            return True
        return False
    
    
    def password_validator(self, password) -> bool:
        if re.fullmatch(PASSWORD_REGEX, password):
            return True
        return False
    
    
    def phone_validator(self, phone) -> bool:
        if re.fullmatch(PHONE_REGEX, phone):
            return True
        return False
    
    
    def aadhaar_validator(self, aadhaar) -> bool:
        if re.fullmatch(AADHAAR_REGEX, aadhaar):
            return True
        return False
    
    
    def licence_validator(self, licence_number) -> bool:
        if re.fullmatch(LICENCE_NUMBER_REGEX, licence_number):
            return True
        return False
    
    
    def zipcode_validator(self, address) -> bool:
        if re.fullmatch(ZIP_CODE_REGEX, address):
            return True
        return False
    
    
regex_validator = RegexValidator()
