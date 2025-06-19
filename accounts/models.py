from django.db import models
from django.core.exceptions import ValidationError
import re

def validate_email(value):
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, value):
        raise ValidationError('Invalid email format.')
    
    if ' ' in value:
        raise ValidationError('Email cannot contain spaces.')
    

class UserAccount(models.Model):
    email = models.EmailField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=100, default='defaultpass123')  # added default

    def clean(self):
        validate_email(self.email)

    def __str__(self):
        return self.email

 
class Product(models.Model):
    product_name = models.CharField(max_length=255, default='Unnamed Product')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    url = models.TextField(default='https://example.com')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)  # optional if user not yet created

    def __str__(self):
        return self.product_name
