import re
import logging
from cheaper.utils.base_validator import BaseValidator

logger = logging.getLogger(__name__)

EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$"
)

class EmailValidator(BaseValidator):
   def validate(self, email: str) -> bool:
    try:
        if not isinstance(email, str):
            logger.warning("Invalid email type: %s", type(email))
            return False

        # Check for leading/trailing spaces before stripping
        if email != email.strip():
            logger.warning("Email has leading or trailing spaces: '%s'", email)
            return False

        email = email.strip()

        if not email:
            logger.warning("Email is empty after stripping.")
            return False

        if ' ' in email:
            logger.warning("Email contains whitespace: '%s'", email)
            return False

        if email.count('@') != 1:
            logger.warning("Email must contain exactly one @ symbol: '%s'", email)
            return False

        local_part, domain_part = email.split('@')
        if not local_part or not domain_part:
            logger.warning("Email missing local or domain part: '%s'", email)
            return False

        if domain_part.startswith('-') or domain_part.startswith('.'):
            logger.warning("Domain starts with invalid character: '%s'", email)
            return False

        if '..' in domain_part:
            logger.warning("Domain has consecutive dots: '%s'", email)
            return False

        if len(domain_part.split('.')[-1]) < 2:
            logger.warning("Top-level domain too short: '%s'", email)
            return False

        if not EMAIL_REGEX.match(email):
            logger.warning("Email does not match regex: '%s'", email)
            return False

        return True

    except Exception as e:
        logger.exception("Unexpected error validating email: %s", e)
        return False
 