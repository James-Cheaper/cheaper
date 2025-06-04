# tests/test_email_validator.py
import pytest
from cheaper.utils.email_validator import EmailValidator

validator = EmailValidator()

def test_valid_emails():
    valid_emails = [
        "user@example.com",
        "firstname.lastname@example.co.uk",
        "user_name+tag@example.com",
    ]
    for email in valid_emails:
        assert validator.validate(email)

def test_invalid_emails():
    invalid_emails = [
        "plainaddress",
        "@missingusername.com",
        "username@-domain.com",
        "username@domain..com",
        "username@domain.c",
        "user@domain@domain.com",
        "",
        " ",
    ]
    for email in invalid_emails:
        assert not validator.validate(email)
