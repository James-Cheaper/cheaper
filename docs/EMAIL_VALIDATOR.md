
# Email Validator Usage

The `EmailValidator` class implements the `BaseValidator` abstract base class and provides a robust `validate()` method to determine if a string is a valid email address.

## Features

- Validates against a strict regex pattern.
- Rejects:
  - Emails with invalid characters or format
  - Emails with double dots (`..`) in the domain
  - Emails with single-letter TLDs (e.g., `example.c`)
  - Emails with leading hyphens in the domain
- Handles edge cases such as:
  - Non-string inputs
  - Empty or whitespace-only strings
- Includes internal exception handling to prevent unexpected crashes during validation

## Validation Rules

The following rules are applied during email validation:

- Must be a non-empty string.
- Must match the regex pattern:
  ```
   r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$"

  ```
- Domain section:
  - Cannot start with a hyphen (`-`)
  - Cannot contain double dots (`..`)
  - TLD must be at least two characters long

## Example

```python
from cheaper.utils.email_validator import EmailValidator

validator = EmailValidator()

# Valid email
print(validator.validate("user@example.com"))  # True

# Invalid formats
print(validator.validate("invalid-email"))     # False
print(validator.validate("user@domain..com"))  # False
print(validator.validate("@missingusername.com"))  # False

# Edge cases
print(validator.validate(""))             # False
print(validator.validate(None))           # False
print(validator.validate(12345))          # False
```

## Testing

Unit tests for the `EmailValidator` class cover a wide range of scenarios including:

-  Valid emails
-  Invalid emails (bad format, special characters, invalid domain structure)
-  Non-string types (e.g., integers, `None`, bytes)
-  Exception scenarios (e.g., regex failure with malformed input)

### Sample Test with `pytest`

```python
def test_valid_emails():
    assert validator.validate("user@example.com")
    assert validator.validate("name.lastname@domain.co")


def test_invalid_not_string():
    assert not validator.validate(None)
    assert not validator.validate(12345)

def test_exception_handling(caplog):
    import logging
    with caplog.at_level(logging.ERROR):
        result = validator.validate(b'\xff')  # Invalid type for regex
        assert not result
        assert "Validation error" in caplog.text
```
