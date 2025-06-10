# cheaper/utils/email_validator.py
import re
import logging
from cheaper.utils.base_validator import BaseValidator

#setup basic logging configuration
logging.basicConfig(level=logging.INFO)

class EmailValidator(BaseValidator):
    """
    EmailValidator validates email strings.

    Usage:
        validator = EmailValidator()
        validator.validate("user@example.com")  # returns True or False
    """
    def validate(self, email: str) -> bool:
        try:
            pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$"
        
            if not isinstance(email, str):
                logging.debug("Validation failed: input is not a string -> %s", email)
                return False
        
            if not email.strip():
                logging.debug("Validation failed: input is empty or whitespace -> '%s'", email)
                return False
        
            if not re.match(pattern, email):
                logging.debug("Validation failed: regex pattern mismatch -> %s", email)
                return False

            if '..' in email:
                logging.debug("Validation failed: email contains consecutive dots -> %s", email)
                return False
       
            return True
    
        except Exception as e:
            logging.error("EmailValidator: Exception occurred while validating '%s': %s", email, e)
            return False
