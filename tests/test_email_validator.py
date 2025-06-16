import pytest
import logging
from cheaper.utils.email_validator import EmailValidator

validator = EmailValidator()

logging.basicConfig(level=logging.INFO)

def test_valid_emails():
    valid_emails = [
        "user@example.com",
        "firstname.lastname@example.co.uk",
        "user_name+tag@example.com",
        "user123@domain-name.org",
        "valid_email@sub.domain.com"
    ]
    for email in valid_emails:
        assert validator.validate(email), f"Should be valid: {email}"

def test_invalid_emails():
    invalid_emails = [
        "plainaddress",                         # No @
        "@missingusername.com",                 # Missing username
        "username@-domain.com",                 # Domain starts with hyphen
        "username@domain..com",                 # Double dots
        "username@domain.c",                    # TLD too short
        "user@domain@domain.com",               # Multiple @
        "",                                     # Empty string
        " ",                                    # Whitespace only
        "user@.com",                            # Starts with dot
        "user @domain.com",                     # Space in email
        "user@ domain.com",                     # Space after @
        "user@domain.com ",                     # Trailing space
        " user@domain.com",                     # Leading space
        None,                                   # Not a string
        12345                                   # Number input
    ]
    for email in invalid_emails:
        assert not validator.validate(email), f"Should be invalid: {email}"
