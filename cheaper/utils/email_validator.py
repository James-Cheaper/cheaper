# cheaper/utils/email_validator.py
import re
from cheaper.utils.base_validator import BaseValidator

class EmailValidator(BaseValidator):
    """
    EmailValidator validates email strings.

    Usage:
        validator = EmailValidator()
        validator.validate("user@example.com")  # returns True or False
    """
    def validate(self, email: str) -> bool:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            return False
        if '..' in email:
            return False
        return True
