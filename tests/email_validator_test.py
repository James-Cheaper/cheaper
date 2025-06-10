# tests/test_email_validator.py
import re
import pytest
import logging
from cheaper.utils.email_validator import EmailValidator

validator = EmailValidator()

def test_valid_emails():
    valid_emails = [
        "user@example.com",
        "firstname.lastname@example.co.uk",
        "user_name+tag@example.com",
    ]
    for email in valid_emails:
        assert validator.validate(email)is True

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
        assert  validator.validate(email)is False


def test_invalid_not_string(caplog):
    with caplog.at_level("DEBUG"):
        assert validator.validate(None) is False
        assert "input is not a string" in caplog.text
        print(caplog.text)

def test_invalid_empty_or_whitespace(caplog):
    with caplog.at_level("DEBUG"):
        assert validator.validate("  ") is False
        assert "input is empty or whitespace" in caplog.text
        print(caplog.text)
        
def test_invalid_regex_mismatch(caplog):
    with caplog.at_level("DEBUG"):
        assert validator.validate("invalid-email") is False
        assert "regex pattern mismatch" in caplog.text
        print(caplog.text)
        
def test_invalid_double_dot(caplog):
    with caplog.at_level("DEBUG"):
        assert validator.validate("user..name@example.com") is False
        assert "contains consecutive dots" in caplog.text
        print(caplog.text)
        
def test_exception_handling(caplog):
    # Temporarily patch regex to force an exception
    import cheaper.utils.email_validator as mod
    original_re_match = re.match
    re.match = lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Test error"))

    with caplog.at_level("ERROR"):
        assert validator.validate("user@example.com") is False
        assert "Exception occurred while validating" in caplog.text
        print(caplog.text)
        
    # Restore original re.match
    re.match = original_re_match