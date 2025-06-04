# Email Validator Usage

The `EmailValidator` class implements the `BaseValidator` abstract base class
and provides a `validate()` method to check if a string is a valid email.

### Example

```python
from cheaper.utils.email_validator import EmailValidator

validator = EmailValidator()
print(validator.validate("user@example.com"))  # True
print(validator.validate("invalid-email"))     # False
