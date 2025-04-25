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
    password = models.CharField(max_length=100)  

    def clean(self):
        validate_email(self.email)

    def __str__(self):
        return self.email

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=10)
    source_url = models.URLField(max_length=150)

    def __str__(self):
        return self.name